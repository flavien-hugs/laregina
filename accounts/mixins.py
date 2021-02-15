# accounts.mixins.py

import datetime
from django.urls import reverse_lazy
from django.db.models import Sum, Avg
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin
)

from core import settings
from catalogue.models import Product
from catalogue.forms import ProductAdminForm
from checkout.models import Order, OrderItem

User = settings.AUTH_USER_MODEL


class CustomerWithOwnerMixin(LoginRequiredMixin):
    """
    Injecte l'utilisateur actuellement connecté
    dans le champ propriétaire du formulaire dans cette vue.
    """

    # TODO: Déterminer la meilleure mise en œuvre
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = User.objects.get(user=self.request.user)
        return form


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Limite l'accès à cette vue à l'utilisateur qui est
    le propriétaire de cet objet (dans une vue d'objet unique).
    """

    # TODO: Augmenter de 404 au lieu de 503
    raise_exception = True

    def test_func(self):
        # Suppose que ceci a un attribut get_object
        # ourrait être testé avec hasattr() ?
        return self.request.user.is_buyer


class UserAccountMixin(LoginRequiredMixin, object):
    product = []
    account = None

    def get_account(self):
        return self.request.user.is_seller

    def get_product(self):
        object_list = Product.objects.filter(user=self.get_account())
        self.product = object_list
        return object_list

    def get_order(self):
        return Order.objects.all()

    def get_order_items(self):
        return OrderItem.objects.filter(product__in=self.get_product())

    def get_order_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        return self.get_order_items().filter(date_created__range=(today_min, today_max))

    def get_total_sale(self):
        total_order_sale = self.get_order_items().aggregate(Sum('price'))
        total_order_price = total_order_sale["price__sum"]
        return total_order_price

    def get_today_sale(self):
        payment = self.get_order_today().aggregate(Sum("price"), Avg("price"))
        total_sale = payment["price__sum"]
        return total_sale


class SellerRequiredMixin(UserAccountMixin, UserPassesTestMixin):
    """
    Limite l'accès de cette vue aux utilisateurs du groupe Vendeur.
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_seller


class UserMixin(SellerRequiredMixin, object):
    def get_object(self):
        return self.get_account()

    def get_object_list(self):
        return self.get_product()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.get_object())


class EditeMixin(SellerRequiredMixin, object):
    pass


class ProductMixin(EditeMixin):
    model = Product


class ProductEditMixin(ProductMixin):
    form_class = ProductAdminForm
    success_url = reverse_lazy('seller:product_list')
    template_name = 'dashboard/seller/includes/_partials_product_create.html'
