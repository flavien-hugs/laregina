import decimal
import datetime
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    UserPassesTestMixin
)

from pages.models import Promotion
from catalogue.models import Product
from catalogue.forms import ProductAdminForm
from checkout.models import Order, OrderItem 


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
        form.instance.user = get_user_model().objects.get(user=self.request.user)
        return form


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user


class SellerTextRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_seller


class SellerRequiredMixin(SellerTextRequiredMixin, object):
    orders = []
    products = []
    account = None

    def get_account(self):
        account = get_user_model().objects.filter(email=self.request.user)
        if account.exists() and account.count() == 1:
            self.account = account.first()
            return account.first()
        return self.request.user

    def get_product(self):
        account = self.get_account()
        object_list = Product.objects.filter(user=account).select_related("user")
        self.products = object_list
        return object_list

    def get_promotion(self):
        account = self.get_account()
        object_list = Promotion.objects.filter(user=account).select_related("user")
        return object_list

    def get_products_count(self):
        product_count = self.get_product().count()
        return product_count

    def get_order_items(self):
        account = self.get_account()
        orders_item_list = OrderItem.objects.filter(
            product__user=account).select_related("order")
        return orders_item_list

    def get_orders_count(self):
        orders_count = self.get_order_items().count()
        return orders_count

    def get_order_account(self):
        account = self.get_account()
        orders_account = OrderItem.objects.filter(
            product__user=account, order=self).select_related("order")
        return orders_account

    # cash du vendeur
    def cash_total(self):
        total = decimal.Decimal('0')
        for item in self.get_order_items():
            total += item.total
        return total

    def get_cost(self):
        percent = decimal.Decimal('0.05')
        cash = self.cash_total() * percent
        return cash

    def cash_total_seller(self):
        total = self.cash_total() - self.get_cost()
        return total

    def get_order_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        return self.get_order_items().filter(date_created__range=(today_min, today_max))

    def get_order_today_count(self):
        order_today_count = self.get_order_today().count()
        return order_today_count
    

class ProductEditMixin(SellerRequiredMixin):
    model = Product
    form_class = ProductAdminForm
    success_url = reverse_lazy('seller:product_list')
