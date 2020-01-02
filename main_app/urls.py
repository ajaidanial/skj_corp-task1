from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("verify/", views.verify_email, name="email verification"),
    path("", RedirectView.as_view(url="login/"), name="redirect-to-login"),
]
