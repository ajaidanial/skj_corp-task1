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
        # TODO: Check for email verified
        login(self.request, user)
        return True, {"form": self.form}


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
        # TODO: Send verification email
        login(self.request, user)
        return True, {"form": self.form}
