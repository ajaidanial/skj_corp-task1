from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView

from main_app.actions import LoginAction, SignUpAction
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

    def post(self, request, *args, **kwargs):
        success, output = SignUpAction(self).execute()
        if not success:
            return self.form_invalid(output["form"])
        return self.form_valid(output["form"])


class HomeView(LoginRequiredMixin, TemplateView):
    """HomeView for user after login."""

    template_name = "main_app/home.html"


@require_http_methods(["GET"])
def verify_email(request):
    """View to verify the emails address."""
    if 'code' in request.GET and 'email' in request.GET:
        code = request.GET['code']
        email = request.GET['email']
        try:
            user = BaseUser.objects.get(username=email)
        except BaseUser.DoesNotExist:
            return redirect(f'{settings.LOGIN_URL}?message="User does not exist.')
        if user.verification_code == code:
            user.verification_code = None
            user.is_email_verified = True
            user.save()
            return redirect(f'{settings.LOGIN_URL}?message="Email verified. Login to continue.')
        return redirect(f'{settings.LOGIN_URL}?message="Invalid verification code.')
    return redirect(settings.LOGIN_URL)


def logout_view(request):
    """logout view."""
    logout(request)
    return redirect(settings.LOGIN_URL)
