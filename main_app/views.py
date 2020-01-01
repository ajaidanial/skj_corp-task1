from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from main_app.actions import LoginAction
from main_app.auth import LogoutRequiredMixin
from main_app.forms import LoginForm, SignUpForm
from main_app.models import BaseUser


class LoginView(LogoutRequiredMixin, FormView):
    """Login View."""

    model = BaseUser
    form_class = LoginForm
    template_name = "main_app/login.html"
    success_url = "."

    def post(self, request, *args, **kwargs):
        success, output = LoginAction(self).execute()
        if not success:
            return self.form_invalid(output["form"])
        return self.form_valid(output["form"])


class SignUpView(LogoutRequiredMixin, FormView):
    """SignUp View."""

    model = BaseUser
    form_class = SignUpForm
    template_name = "main_app/signup.html"
    success_url = "."

    def form_valid(self, form):
        # TODO: signup action
        self.object = form.save()
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    """HomeView for user after login."""

    template_name = "main_app/home.html"


def logout_view(request):
    """logout view."""
    logout(request)
    return redirect(settings.LOGIN_URL)
