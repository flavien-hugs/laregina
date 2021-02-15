# accounts.views.seller.py

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    FormView, CreateView, DeleteView,
    DetailView, RedirectView, ListView,
    UpdateView
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from cart import cart
from ..models import User
from catalogue.models import Product
from checkout.models import Order, OrderItem

from ..forms import MarketSignupForm, StoreUpdateForm
from ..mixins import UserAccountMixin, SellerRequiredMixin, ProductEditMixin


class ProfileDetailView(SellerRequiredMixin, DetailView):
    model = User
    template_name = 'dashboard/seller/index.html'
    extra_context = {'user_type': 'seller'}

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = self.object.store
        kwargs['order_list_today'] = self.get_order_today()
        kwargs['order_list'] = self.get_order()
        kwargs['product_list'] = self.get_product()
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_buyer:
                return redirect('customer:customer_dashboard')
            elif request.user.is_anonymous:
                return redirect('/')
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.get_order()


# même chose que ci-dessus, mais pour voir un autre vendeur.
class StoreDetailView(DetailView):
    model = User
    template_name='dashboard/seller/includes/_partials_vendor_store.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = 'Magasin : {store_name}'.format(store_name=self.object.store)
        kwargs['object_list'] = Product.objects.filter(user=self.object.id)
        return super().get_context_data(*args, **kwargs)


# update a profile.
class SettingsUpdateView(SellerRequiredMixin, UpdateView):
    model = User
    form_class = StoreUpdateForm
    template_name = 'dashboard/seller/includes/_partials_settings_store.html'
    success_url = reverse_lazy('seller:profile')

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = 'Configuration de votre boutique : {store}'.format(
            store=self.object.store)
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        message = """Votre compte a été mise à jour avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserProductDetailRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, slug=kwargs['slug'])
        return obj.get_absolute_url()

class OrderListView(SellerRequiredMixin, ListView):
    paginate_by = 50
    template_name = 'dashboard/seller/includes/_partials_orders_list.html'

    def get_context_data(self, **kwargs):
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.get_order()


class OrderDetailView(SellerRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/seller/includes/_partials_orders_list.html'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Commande N°: {transaction_id}'.format(
            transaction_id=self.object.transaction_id)
        kwargs['total_sale'] = self.get_total_sale()
        kwargs['cart_subtotal']= cart.cart_subtotal(self.request),
        return super().get_context_data(**kwargs)


class ProductListView(SellerRequiredMixin, ListView):
    paginate_by = 50
    template_name = 'dashboard/seller/includes/_partials_product_list.html'
    permission_required = 'product.product_list'

    def get_queryset(self):
        return self.get_product()

    def get_context_data(self, **kwargs):
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(**kwargs)


class ProductPermView(PermissionRequiredMixin, ProductEditMixin):
    pass


class ProductCreateView(ProductPermView, CreateView):
    permission_required = 'product.product_create'

    def form_valid(self, form):
        message = """Votre nouveau produit a été ajouté  avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(**kwargs)


class ProductUpdateView(ProductPermView, UpdateView):
    permission_required = 'product.update_product'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Mise à jour du produit: {}'.format(self.object.name)
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        message = """Votre produit a été mise à jour avec succes !"""
        messages.success(self.request, message)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDeleteView(ProductPermView, DeleteView):
    permission_required = 'product.product_delete'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Supprimer ce produit: {}'.format(
            str(self.object.name))
        kwargs['total_sale'] = self.get_total_sale()
        return super().get_context_data(**kwargs)
