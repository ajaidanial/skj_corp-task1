from django.forms import ModelForm

from main_app.models import BaseUser


class LoginForm(ModelForm):
    """Form to login user."""

    class Meta:
        model = BaseUser
        fields = [
            "email",
            "password",
        ]

    def clean(self):
        self._validate_unique = False
        return self.cleaned_data


class SignUpForm(ModelForm):
    """Form to signup user."""

    class Meta:
        model = BaseUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
        ]
