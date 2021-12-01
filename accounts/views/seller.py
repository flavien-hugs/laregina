# accounts.views.seller.py

from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin

from core import settings
from catalogue.models import Product
from checkout.models import Order, OrderItem
from catalogue.forms import ProductCreateFormSet

from accounts.models import ProfileSocialMedia
from accounts.mixins import SellerRequiredMixin, ProductEditMixin
from accounts.forms import MarketSignupForm, StoreUpdateForm, SocialMediaForm


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
        kwargs['subtitle'] = "dashboard"
        kwargs['page_title'] = self.object.store
        kwargs['order_list'] = self.get_order_items()
        kwargs['product_list'] = self.get_product()
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.get_object())


dashboard_view = DashboardView.as_view()


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
    slug_field = "slug"
    slug_url_kwarg = "slug"
    model = get_user_model()
    template_name='dashboard/seller/includes/_partials_vendor_store.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['page_title'] = f'Boutique : {self.object.store}'
        kwargs['object_list'] = Product.objects.filter(user=self.object.id)
        return super().get_context_data(*args, **kwargs)


store_detail_view = StoreDetailView.as_view()


class SettingsUpdateView(
    SellerRequiredMixin,
    CashTotalSeller,
    SuccessMessageMixin,
    generic.UpdateView
):
    slug_field = "slug"
    slug_url_kwarg = "slug"
    model = get_user_model()
    form_class = StoreUpdateForm
    success_message = "Votre profile a été mise à jour avec succes !"
    template_name = 'dashboard/seller/includes/_partials_settings_store.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_context_data(self, *args, **kwargs):
        kwargs['subtitle'] = "Réglages"
        kwargs['page_title'] = f'Configuration de votre boutique : {self.object.store}'
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        msg = 'Votre profile a été mise à jour avec succes !'
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'seller:update',
            kwargs={'slug': self.get_object().slug}
        )


settings_view = SettingsUpdateView.as_view()


class SocialMediaUpdateView(
    SellerRequiredMixin,
    CashTotalSeller,
    generic.UpdateView
):
    model = ProfileSocialMedia
    form_class = SocialMediaForm
    template_name = 'dashboard/seller/includes/_partials_settings_media.html'
    success_url = None

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_context_data(self, *args, **kwargs):
        kwargs['subtitle'] = "Logo & Profile réseaux sociaux"
        kwargs['page_title'] = 'Mettre à jour vos profile réseaux sociaux'
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        msg = 'Votre votre profile réseaux sociaux a été mise à jour avec succès !'
        messages.success(self.request, msg)
        return super(SocialMediaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'seller:rs_update',
            kwargs={'slug': self.get_object().slug}
        )


social_media_view = SocialMediaUpdateView.as_view()


class OrderListView(SellerRequiredMixin, CashTotalSeller, generic.ListView):
    paginate_by = 10
    template_name = 'dashboard/seller/includes/_partials_orders_list.html'

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_queryset(self):
        return self.get_order_items()

    def get_context_data(self, **kwargs):
        kwargs['subtitle'] = "vos commandes"
        kwargs['page_title'] = "liste des vos commandes"
        return super().get_context_data(**kwargs)


order_list_view = OrderListView.as_view()


class OrderDetailView(SellerRequiredMixin, CashTotalSeller, generic.DetailView):
    model = Order
    template_name = 'dashboard/seller/includes/_partials_orders_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['subtitle'] = "commande"
        kwargs['page_title'] = f'commande N°: {self.object.transaction_id}'
        return super().get_context_data(**kwargs)


order_detail_view = OrderDetailView.as_view()


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
        kwargs['page_title'] = "vos produits"
        kwargs['subtitle'] = "liste de vos produits"
        return super().get_context_data(*args, **kwargs)


product_list_view = ProductListView.as_view()


class ProductCreateView(
    ProductEditMixin, CashTotalSeller, generic.CreateView
):
    
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
        msg = 'Votre nouveau produit a été ajouté  avec succes !'
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


    def get_context_data(self, *args, **kwargs):
        kwargs['subtitle'] = "ajouter un nouveau produit"
        kwargs['page_title'] = "ajouter un nouveau produit"
        return super().get_context_data(*args, **kwargs)


product_create_view = ProductCreateView.as_view()


class ProductUpdateView(
    ProductEditMixin, CashTotalSeller,
    generic.UpdateView
):
    
    template_name = 'dashboard/seller/includes/_partials_product_create.html'

    def get_context_data(self, **kwargs):
        kwargs['subtitle'] = f"mise à jour du produit '{self.object.name}'"
        kwargs['page_title'] = f"mise à jour du produit '{self.object.name}'"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        msg = f'Mise à jour du produit "{self.object.name}" effectuée avec succes !'
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())


product_update_view = ProductUpdateView.as_view()


class ProductDeleteView(
    ProductEditMixin, CashTotalSeller,
    generic.DeleteView
):
    permission_required = 'product.product_delete'

    def form_valid(self, form):
        msg = f'"{self.object.name}" supprimé avec succes !'
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())


product_delete_view = ProductDeleteView.as_view()
