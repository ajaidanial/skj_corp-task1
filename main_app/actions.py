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
        login(self.request, user)
        return True, {"form": self.form}
