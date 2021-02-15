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
    
    """
    prend une demande POST contenant des données de commande valides,
    envoie à la passerelle de paiement les informations de facturation
    et renvoie un dictionnaire Python avec deux entrées : "numéro_de_commande"
    et "message" en fonction du succès du traitement du paiement.
    Une facturation non réussie aura un numéro de commande de 0 et
    une erreur avec un numéro de commande et un message de chaîne vide.
    """
    
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    
    postdata = request.POST.copy()
    amount = cart.cart_subtotal(request)
    
    results = {}
    
    if response[0] == APPROVED:
        transaction_id = response[0]
        order = create_order(request, transaction_id)
        results = {'order_number': order.id, 'message': ''}
    if response[0] == DECLINED:
        results = {'order_number': 0, 'message': 'Il y a un problème avec votre carte de crédit.'}
    if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number': 0, 'message': 'Erreur de traitement de votre commande.'}
    return results


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
    
    # order.transaction_id = transaction_id
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
            order_item.price = cart_item.price
            order_item.product = cart_item.product
            order_item.save()
        
        # tout est prêt, videz le chariot
        cart.empty_cart(request)
    return order
