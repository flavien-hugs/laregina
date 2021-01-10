# accounts.views.customer.py

from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from ..models import User
from ..forms import CustomerInterestsForm, CustomerSignUpForm


# @method_decorator([login_required, buyer_required], name='dispatch')
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'account/signup.html'
    success_url = 'list'

    extra_context = {'user_type': 'buyer'}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list')