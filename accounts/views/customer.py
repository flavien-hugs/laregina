# accounts.views.customer.py

from django.urls import reverse
from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from ..models import User
from ..forms import CustomerSignUpForm


# @method_decorator([login_required, buyer_required], name='dispatch')
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'account/signup.html'
    extra_context = {'user_type': 'buyer'}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:
                return redirect('customer:customer_dashboard')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer:customer_dashboard')
