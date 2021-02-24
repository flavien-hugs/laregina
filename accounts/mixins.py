# accounts.mixins.py

import decimal
import datetime
from django.urls import reverse_lazy
from django.db.models import Sum, Avg
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    UserPassesTestMixin
)

from catalogue.models import Product
from catalogue.forms import ProductAdminForm
from checkout.models import Order, OrderItem

User = get_user_model()


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "home"

    def get_next_url(self):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, self.request.get_host()):
            return redirect_path
        return self.default_next


class CustomerWithOwnerMixin(LoginRequiredMixin):
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = User.objects.get(user=self.request.user.is_buyer)
        return form


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_buyer


class SellerTextRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_seller


class SellerRequiredMixin(SellerTextRequiredMixin, object):
    orders = []
    products = []
    account = None

    def get_account(self):
        account = User.objects.filter(email=self.request.user)
        if account.exists() and account.count() == 1:
            self.account = account.first()
            return account.first()
        return self.request.user

    def get_product(self):
        account = self.get_account()
        object_list = Product.objects.filter(user=account)
        self.products = object_list
        return object_list

    def get_order_items(self):
        products = self.get_product()
        order_items = OrderItem.objects.filter(product__in=products)
        return order_items

    def get_order(self):
        order_list = Order.objects.all()
        return order_list

    def get_order_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        return self.get_order_items().filter(date_created__range=(today_min, today_max))

    def get_total_sale(self):
        total = decimal.Decimal(0)
        orders = self.get_order_items()
        for item in orders:
            total += item.total_order()
        return total

    def get_today_sale(self):
        order_sale = self.get_order_today().aggregate(Sum("price__sum"))
        total_sale = order_sale["price__sum"]
        return total_sale


class ProductMixin(SellerRequiredMixin):
    model = Product
    form_class = ProductAdminForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

class ProductEditMixin(ProductMixin):
    success_url = reverse_lazy('seller:product_list')
    template_name = 'dashboard/seller/includes/_partials_product_create.html'
