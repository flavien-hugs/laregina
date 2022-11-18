# checkout.checkout.py

from django.urls import reverse

from cart import cart
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from analytics.utils import get_client_ip


def get_checkout_url(request):
    return reverse("checkout:checkout")


def process(request):

    order = create_order(request)
    context = {
        "order": order,
        "payment": order.payment,
        "order_id": order.transaction_id,
    }
    return context


def create_order(request):

    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)

    order.ip_address = get_client_ip(request)
    order.user = None

    if request.user.is_authenticated:
        order.user = request.user

    order.status = Order.SUBMITTED
    order.save()

    if order.pk:
        cart_items = cart.get_cart_items(request)

        for cart_item in cart_items:
            order_item = OrderItem()
            order_item.order = order
            order_item.quantity = cart_item.quantity
            order_item.product = cart_item.product
            order_item.save()
        cart.empty_cart(request)
    return order
