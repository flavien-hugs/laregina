# accounts.views.customer.py

from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..models import User
from ..forms import CustomerSignUpForm


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'account/signup.html'
    extra_context = {'user_type': 'buyer'}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:
                return redirect('catalogue:product_list')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('catalogue:product_list')
