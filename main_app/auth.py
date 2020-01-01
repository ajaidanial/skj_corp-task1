from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LogoutRequiredMixin(AccessMixin):
    """Redirect to HOME_URL if user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.HOME_URL)
        return super().dispatch(request, *args, **kwargs)
