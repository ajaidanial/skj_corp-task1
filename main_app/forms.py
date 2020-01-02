from django import forms
from django.core.exceptions import ValidationError

from main_app.models import BaseUser


class LoginForm(forms.ModelForm):
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


class SignUpForm(forms.ModelForm):
    """Form to signup user."""

    confirm_password = forms.CharField(max_length=128)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = BaseUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "confirm_password",
        ]

    def clean_confirm_password(self):
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise ValidationError("Does not match your password.", code="invalid")
        return self.cleaned_data["confirm_password"]
