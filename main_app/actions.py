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
        self.form.errors[NON_FIELD_ERRORS] = self.form.error_class(
            ["Verification email sent. Verify your email and then login."]
        )
        return False, {"form": self.form}

    def send_verification_email(self, user):
        sender_address = settings.SENDER_MAIL_CREDENTIALS["address"]
        sender_password = settings.SENDER_MAIL_CREDENTIALS["password"]
        if sender_address and sender_password:
            # TODO: Send verification email
            pass
        else:
            # credentials are not provided
            user.is_email_verified = True
            user.save()
