from functools import wraps

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class NotACustomerException(PermissionDenied):
    pass


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated and user.is_customer and user.is_active:
            return True
        raise NotACustomerException(
            "Accès refusé. Vous n'êtes pas un client ou votre compte n'est pas activé."
        )


def login_required_redirect(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
