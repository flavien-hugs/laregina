# accounts.views.customer.py


from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from ..models import User
from ..forms import CustomerInterestsForm, CustomerSignUpForm


# @method_decorator([login_required, buyer_required], name='dispatch')
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'buyer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list')
