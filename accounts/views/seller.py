# accounts.views.seller.py

from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView,
    DetailView, RedirectView,
    ListView, UpdateView
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from cart import cart
from catalogue.models import Product
from checkout.models import Order, OrderItem
from catalogue.forms import ProductAdminForm, ProductCreateFormSet

User = get_user_model()

from ..forms import MarketSignupForm, StoreUpdateForm
from ..mixins import SellerRequiredMixin, ProductEditMixin


class CashTotalSeller(object):

    def get_context_data(self, *args, **kwargs):
        # kwargs['cost'] = self.get_cost()
        kwargs['orders_count'] = self.get_orders_count()
        kwargs['order_list_today'] = self.get_order_today()
        kwargs['order_today_count'] = self.get_order_today_count()
        kwargs['product_count'] = self.get_products_count()
        kwargs['cash_total_seller'] = self.cash_total_seller()
        return super().get_context_data(*args, **kwargs)


class DashboardView(SellerRequiredMixin, CashTotalSeller, DetailView):
    model = User
    template_name = 'dashboard/seller/index.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = self.object.store
        kwargs['order_list'] = self.get_order_items()
        kwargs['product_list'] = self.get_product()
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.get_object())


# même chose que ci-dessus, mais pour voir un autre vendeur.
class StoreDetailView(DetailView):
    model = User
    template_name='dashboard/seller/includes/_partials_vendor_store.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = 'Magasin : {store_name}'.format(store_name=self.object.store)
        kwargs['object_list'] = Product.objects.filter(user=self.object.id)
        return super().get_context_data(*args, **kwargs)


# update a profile.
class SettingsUpdateView(SellerRequiredMixin, CashTotalSeller, UpdateView):
    form_class = StoreUpdateForm
    template_name = 'dashboard/seller/includes/_partials_settings_store.html'
    success_url = reverse_lazy('seller:profile')

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = 'Configuration de votre boutique : {store}'.format(
            store=self.object.store)
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        message = """Votre compte a été mise à jour avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class OrderListView(SellerRequiredMixin, CashTotalSeller, ListView):
    paginate_by = 10
    template_name = 'dashboard/seller/includes/_partials_orders_list.html'

    def get_queryset(self):
        return self.get_order_items()


class OrderDetailView(SellerRequiredMixin, CashTotalSeller, DetailView):
    model = Order
    template_name = 'dashboard/seller/includes/_partials_orders_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Commande N°: {transaction_id}'.format(
            transaction_id=self.object.transaction_id)
        return super().get_context_data(**kwargs)


class ProductListView(SellerRequiredMixin, CashTotalSeller, ListView):
    paginate_by = 10
    template_name = 'dashboard/seller/includes/_partials_product_list.html'
    permission_required = 'product.product_list'

    def get_queryset(self):
        return self.get_product().order_by('-created_at')


class ProductCreateView(ProductEditMixin, CashTotalSeller, CreateView):

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(form=form)
        formset = context['image_formset']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        message = """Votre nouveau produit a été ajouté  avec succes !"""
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        if self.request.POST:
            kwargs['image_formset'] = ProductCreateFormSet(self.request.POST, self.request.FILES)
        else:
            kwargs['image_formset'] = ProductCreateFormSet()
        return super().get_context_data(**kwargs)


class ProductUpdateView(ProductEditMixin, UpdateView):

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Mise à jour du produit: {}'.format(self.object.name)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        message = """Votre produit a été mise à jour avec succes !"""
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class ProductDeleteView(ProductEditMixin, DeleteView):
    permission_required = 'product.product_delete'
    template_name = 'dashboard/seller/includes/_partials_product_delete.html'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Supprimer ce produit: {}'.format(
            str(self.object.name))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        message = """Le produit a été retiré de votre magasin avec succes !"""
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())
