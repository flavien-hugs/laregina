# accounts.views.customer.py

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.models import Group

from ..forms import CustomerSignUpForm
from ..mixins import NextUrlMixin, RequestFormAttachMixin


class CustomerSignUpView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = CustomerSignUpForm
    template_name = 'account/customer_signup.html'
    default_next = reverse_lazy('customer_signup')

    def get_success_url(self):
        return self.get_next_url()

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.default_next)