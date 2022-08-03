# checkout.checkout.py

import requests

from django.urls import reverse
from django.conf import settings

from cart import cart
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from analytics.utils import get_client_ip


def get_checkout_url(request):
    return reverse('checkout:checkout')

def process(request):

    order = create_order(request)
    context = {
        'order': order,
        'payment': order.payment,
        'order_id': order.transaction_id,
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

        """ si la sauvegarde de la commande a réussi """
        cart_items = cart.get_cart_items(request)

        for cart_item in cart_items:
            """
            créer un article de commande pour chaque article du panier
            """
            order_item = OrderItem()
            order_item.order = order
            order_item.quantity = cart_item.quantity
            order_item.product = cart_item.product
            order_item.save()

        # tout est prêt, videz le chariot
        cart.empty_cart(request)
    return order


def send_sms_order(order_id):

    SENDER_ID = settings.SENDER_ID
    SMS_API_KEY = settings.SMS_API_KEY

    order = Order.objects.get(transaction_id=order_id)
    order_transaction_id = order.transaction_id
    destinataire = order.phone
    message = f"Bonjour, votre commande {order_transaction_id} a été validée avec succès. Merci pour votre achat sur laregina.deals."

    SEND_SMS_URL = f"https://sms.lws.fr/sms/api?action=send-sms&api_key={SMS_API_KEY}&to={destinataire}&from={SENDER_ID}&sms={message}"

    response = requests.post(SEND_SMS_URL)
    print(response)
    return response
