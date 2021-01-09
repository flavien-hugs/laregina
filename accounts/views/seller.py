# accounts.views.seller.py

from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView, CreateView, DeleteView, DetailView, RedirectView, ListView, UpdateView

from ..models import User
from ..forms import MarketSignupForm, StoreProfileUpdateForm
from ..mixins import OwnerRequiredMixin, SellerRequiredMixin


# class SellerSignUpView(CreateView):
#     model = User
#     form_class = MarketSignupForm
#     template_name = 'account/signup.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'seller'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('accounts:profile')


class StoreProfileSelfDetailView(SellerRequiredMixin, DetailView):
    model = User
    template_name = 'seller_dashboard/index.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts_list'] = Post.objects.filter(owner=self.request.profile).order_by("-modified")
    #     context['reviews_list'] = Review.objects.filter(reviewee=self.request.profile).order_by("-modified")
    #     if len(context['reviews_list']) > 0:
    #         average = context['reviews_list'].aggregate(Avg('score'))['score__avg']
    #     else:
    #         average = 0
    #     average_str = []
    #     val = 0.00
    #     ''' Django HTML has a hard time looping through numerical values, so to display the score
    #     we convert it to a string, (5 stars is 'fffff', 0 is 'eeeee') and then iterate through the
    #     string to display stars on a seller's page. Hacky to be sure, but I wasn't able to find a
    #     more elegant alternative'''
    #     while val < 5:
    #         if val + 1 <= average:
    #             average_str.append('f')
    #         elif val + 0.5 <= average:
    #             average_str.append('h')
    #         else:
    #             average_str.append('e')
    #         val += 1
    #     context['average_str'] = average_str
    #     context['average'] = average
    #     return context



# Même chose que ci-dessus, mais pour voir un autre vendeur.
class StoreProfileDetailView(DetailView):
    model = User
    template_name = 'seller_dashboard/index.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = SocialProfile.objects.get(slug=self.kwargs['slug']).owner
    # class SocialProfileSelfDetailView(SellerRequiredMixin, DetailView):
    # context['posts_list'] = Post.objects.filter(owner=user).order_by("-modified")
    #     context['reviews_list'] = Review.objects.filter(reviewee=user).order_by("-modified")
    #     if len(context['reviews_list']) > 0:
    #         average = context['reviews_list'].aggregate(Avg('score'))['score__avg']
    #     else:
    #         average = 0
    #     average_str = []
    #     val = 0.00
    #     while val < 5:
    #         if val + 1 <= average:
    #             average_str.append('f')
    #         elif val + 0.5 <= average:
    #             average_str.append('h')
    #         else:
    #             average_str.append('e')
    #         val += 1
    #     context['average_str'] = average_str
    #     context['average'] = average
    #     return context


# Update a profile.
class StoreProfileUpdateView(SellerRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = User
    form_class = StoreProfileUpdateForm
    template_name = 'seller_dashboard/layouts/settings-store.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Seller profile updated!', extra_tags='fa fa-check')
        return reverse('seller:profile')