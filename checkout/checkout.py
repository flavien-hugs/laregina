# checkout.checkout.py

import urllib
from django.urls import reverse

from cart import cart
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from analytics.utils import get_client_ip


def get_checkout_url(request):
    
    """
    renvoie l'URL du module de paiement pour le panier
    """
    
    # l'utiliser pour notre propre vérification sur place
    return reverse('checkout:checkout')


def process(request):
    
    order = create_order(request)
    context = {
        'order_id': order.transaction_id,
    }
    return context


def create_order(request):

    """
    si la POST de la passerelle de paiement a réussi
    à facturer le client, créer une nouvelle commande
    contenant chaque instance de CartItem, enregistrer
    la commande avec l'ID de transaction de la passerelle
    et vider le panier
    """

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
