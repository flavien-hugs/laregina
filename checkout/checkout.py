# checkout.checkout.py


import requests

from django.urls import reverse
from django.conf import settings

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

    SENDER_ID = settings.SENDER_ID
    SMS_API_KEY = settings.SMS_API_KEY
    SMS_API_TOKEN = settings.API_TOKEN

    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)

    order.user = None
    order.ip_address = get_client_ip(request)

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

            DESTINATAIRE = "2250160011585"
            MESSAGE = f"Bonjour, Vous avez une commande sur {settings.SITE_NAME}."

            SEND_SMS_URL = f"https://panel.smsing.app/smsAPI?sendsms&apikey={SMS_API_KEY}&apitoken={SMS_API_TOKEN}&type=sms&from={SENDER_ID}&to={DESTINATAIRE}&text={MESSAGE}"
            requests.request("POST", SEND_SMS_URL)
            order_item.save()
        cart.empty_cart(request)
    return order
