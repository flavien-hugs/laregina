# accounts.views.seller.py

from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView, CreateView, DeleteView, DetailView, RedirectView, ListView, UpdateView

from ..models import User
from ..forms import MarketSignupForm, StoreUpdateForm
from ..mixins import CustomerWithOwnerMixin, SellerRequiredMixin, UserAccountMixin


class StoreProfileDetailView(SellerRequiredMixin, UserAccountMixin, DetailView):
    model = User
    template_name = 'dashboard/seller/index.html'
    extra_context = {'user_type': 'seller'}

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = self.object.store
        return super().get_context_data(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_buyer:
                return redirect('customer:customer_dashboard')
            elif request.user.is_anonymous:
                return redirect('/')
            elif request.user.is_superuser:
                return redirect('/admin/')
        return super().dispatch(self.request, *args, **kwargs)

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
class StoreDetailView(DetailView):
    model = User
    template_name='dashboard/seller/layouts/vendor-store.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = self.object.store
        return super().get_context_data(*args, **kwargs)


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
class StoreUpdateView(SellerRequiredMixin, UpdateView):
    model = User
    form_class = StoreUpdateForm
    template_name = 'dashboard/seller/layouts/settings-store.html'
    success_url = reverse_lazy('seller:profile')

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = 'Configuration boutique : {}'.format(self.object.store)
        return super().get_context_data(*args, **kwargs)
