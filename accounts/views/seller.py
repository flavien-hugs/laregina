# accounts.views.seller.py

from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from core import settings
from catalogue.models import Product
from checkout.models import Order, OrderItem
from catalogue.forms import ProductCreateFormSet

from ..forms import MarketSignupForm, StoreUpdateForm
from ..mixins import SellerRequiredMixin, ProductEditMixin


class CashTotalSeller(object):

    def get_context_data(self, *args, **kwargs):
        kwargs['orders_count'] = self.get_orders_count()
        kwargs['order_list_today'] = self.get_order_today()
        kwargs['order_today_count'] = self.get_order_today_count()
        kwargs['product_count'] = self.get_products_count()
        kwargs['cash_total_seller'] = self.cash_total_seller()
        return super().get_context_data(*args, **kwargs)


class DashboardView(SellerRequiredMixin, CashTotalSeller, generic.DetailView):
    template_name = 'dashboard/seller/index.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = self.object.store
        kwargs['order_list'] = self.get_order_items()
        kwargs['product_list'] = self.get_product()
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.get_object())


class StoreListView(generic.ListView):
    paginate_by = 180
    context_object_name = 'vendor_list_object'
    queryset = get_user_model().objects.order_by('-date_joined')
    template_name = 'includes/partials/_partials_vendor_list.html'

    def head(self, *args, **kwargs):
        last_vendor_register = self.get_queryset().latest('-date_joined')
        response = HttpResponse()
        response['Last-Modified'] = last_vendor_register.date_joined.strftime(
            '%a, %d %b %Y %H:%M:%S GMT')
        return response


store_list_view = StoreListView.as_view(extra_context={'page_title': 'boutiques'})


class StoreDetailView(generic.DetailView):
    model = get_user_model()
    template_name='dashboard/seller/includes/_partials_vendor_store.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = f'Boutique : {self.object.store}'
        kwargs['object_list'] = Product.objects.filter(user=self.object.id)
        return super().get_context_data(*args, **kwargs)


store_detail_view = StoreDetailView.as_view()


# update a profile.
class SettingsUpdateView(SellerRequiredMixin, CashTotalSeller, generic.UpdateView):
    model = get_user_model()
    form_class = StoreUpdateForm
    template_name = 'dashboard/seller/includes/_partials_settings_store.html'
    success_url = reverse_lazy('seller:profile')

    def get_object(self, *args, **kwargs):
        return self.get_account()

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


class OrderListView(SellerRequiredMixin, CashTotalSeller, generic.ListView):
    paginate_by = 15
    template_name = 'dashboard/seller/includes/_partials_orders_list.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_queryset(self):
        return self.get_order_items()

class OrderDetailView(SellerRequiredMixin, CashTotalSeller, generic.DetailView):
    model = Order
    template_name = 'dashboard/seller/includes/_partials_orders_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = f'Commande N°: {self.object.transaction_id}'
        return super().get_context_data(**kwargs)


class ProductListView(SellerRequiredMixin, CashTotalSeller, generic.ListView):
    paginate_by = 15
    permission_required = 'product.product_list'
    template_name = 'dashboard/seller/includes/_partials_product_list.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_queryset(self):
        return self.get_product()

    def get_context_data(self, *args, **kwargs):
        kwargs['object_list'] = self.get_product()
        return super().get_context_data(*args, **kwargs)


class ProductCreateView(ProductEditMixin, CashTotalSeller, generic.CreateView):

    template_name = 'dashboard/seller/includes/_partials_product_create.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = ProductCreateFormSet()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset
            )
        )

    def post(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = ProductCreateFormSet(self.request.POST, self.request.FILES)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.instance.user = self.request.user
        self.object = form.save()

        formset.instance = self.object
        formset.save()

        message = """Votre nouveau produit a été ajouté  avec succes !"""
        messages.success(self.request, message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductUpdateView(ProductEditMixin, CashTotalSeller, generic.UpdateView):

    template_name = 'dashboard/seller/includes/_partials_product_create.html'

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


class ProductDeleteView(ProductEditMixin, CashTotalSeller, generic.DeleteView):
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
