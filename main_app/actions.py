import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import NON_FIELD_ERRORS


class LoginAction:
    """Action to take care of LoginView"""

    def __init__(self, view, *args, **kwargs):
        self.request = view.request
        self.form = view.get_form()

    def execute(self):
        if not self.form.is_valid():
            return False, {"form": self.form}
        user = authenticate(
            self.request,
            username=self.form.cleaned_data["email"],
            password=self.form.cleaned_data["password"],
        )
        if not user:
            self.form.errors[NON_FIELD_ERRORS] = self.form.error_class(
                ["Unable to login with given credentials."]
            )
            return False, {"form": self.form}
        # check if user's emails is verified
        if user.is_email_verified:
            login(self.request, user)
            return True, {"form": self.form}
        self.form.errors[NON_FIELD_ERRORS] = self.form.error_class(
            ["Email address not yet verified."]
        )
        return False, {"form": self.form}


class SignUpAction:
    """Action to take care of SignUpView"""

    def __init__(self, view, *args, **kwargs):
        self.request = view.request
        self.form = view.get_form()
        self.model = self.form._meta.model

    def execute(self):
        if not self.form.is_valid():
            return False, {"form": self.form}
        data = self.form.cleaned_data
        user = self.model.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            avatar=data["avatar"],
        )
        self.send_verification_email(user)
        if user.is_email_verified:
            login(self.request, user)
            return True, {"form": self.form}
        self.form = self.form.__class__()
        self.form.errors[NON_FIELD_ERRORS] = self.form.error_class(
            ["Verification email sent. Verify your email and then login."]
        )
        return False, {"form": self.form}

    def send_verification_email(self, user):
        sender_address = settings.SENDER_MAIL_CREDENTIALS["address"]
        sender_password = settings.SENDER_MAIL_CREDENTIALS["password"]
        link_to_revert = settings.SENDER_MAIL_CREDENTIALS["link_to_revert"]
        if sender_address and sender_password:
            """Credentials are provided. Send the email."""
            # make verification code
            user.verification_code = self.generate_verification_code()
            # gmail session
            gmail_session = smtplib.SMTP("smtp.gmail.com", 587)
            gmail_session.ehlo()
            gmail_session.starttls()
            gmail_session.ehlo()
            gmail_session.login(sender_address, sender_password)
            # message to be sent
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = user.email
            message["Subject"] = "Verify Your Email Address"
            mail_body = (
                "Hello {name},<br />"
                "Click the link below to verify your email address.<br />"
                "<a href='{link_to_revert}?code={code}&email={email}'>Verify email.</a>"
            ).format(
                name=user.first_name,
                code=user.verification_code,
                link_to_revert=link_to_revert,
                email=user.email,
            )
            message.add_header("reply-to", sender_address)
            message.attach(MIMEText(mail_body, "html"))
            # send the email
            gmail_session.sendmail(sender_address, user.email, message.as_string())
        else:
            # credentials are not provided
            user.is_email_verified = True
        user.save()

    def generate_verification_code(self, size=10, chars=string.digits):
        """Returns a random string of numbers based on the given `size`."""
        return "".join(random.choice(chars) for _ in range(size))
