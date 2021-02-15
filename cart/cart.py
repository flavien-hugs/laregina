# cart.cart.py

import random
from decimal import Decimal
from django.db.models import Max
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from core.utils import generate_key

from cart.models import CartItem
from catalogue.models import Product


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):

    """
    obtenir l'identifiant du chariot de l'utilisateur actuel,
    en définir un nouveau si vide;
    Note: la syntaxe ci-dessous correspond au texte,
    mais une autre façon, plus claire, de vérifier l'ID du panier serait la suivante:
    
    if not CART_ID_SESSION_KEY in request.session:
    """

    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():

    """
    fonction permettant de générer des valeurs
    d'identification aléatoires du chariot
    """

    cart_id = ''
    characters = '1234567890'
    cart_id_length = 50
    for cart_id in range(cart_id_length):
        cart_id = characters[random.randint(0, len(characters)-1)]
    return cart_id


def get_cart_items(request):

    """
    restituer tous les objets du chariot de l'utilisateur actuel
    """
    return CartItem.objects.filter(cart_id=_cart_id(request),)


def add_to_cart(request):

    """
    fonction qui prend une demande de POST
    et ajoute une instance de produit au panier du client actuel
    """

    postdata = request.POST.copy()

    # obtenir l'url du produit à partir des données POST,
    # renvoyer en blanc si elle est vide
    slug = postdata.get('slug', '')

    # obtenir la quantité ajoutée, renvoyer 1 si vide
    quantity = postdata.get('quantity', 1)

    # aller chercher le produit ou renvoyer une erreur de page manquante
    p = get_object_or_404(Product, slug=slug)
    
    # obtenir des produits dans le panier
    cart_products = get_cart_items(request)
    product_in_cart = False

    # vérifier si l'article est déjà dans le panier
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # mettre à jour la quantité si elle est trouvée
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        # créer et enregistrer un nouvel article dans le panier
        cartitem = CartItem()
        cartitem.product = p
        cartitem.quantity = quantity
        cartitem.cart_id = _cart_id(request)
        cartitem.save()

        
def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request)) 


def update_cart(request):

    """ 
    mettre à jour la quantité pour un seul article :
    la fonction prend une demande POST qui met à jour
    la quantité pour un produit unique dans le panier du client actuel   
    """

    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


def remove_from_cart(request):
    
    """
    retirer un seul article du panier :
    la fonction qui prend une demande de POST
    supprime une instance de produit unique du panier d'achat du client actuel
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):

    """ 
    obtenir le sous-total pour un article dans le panier
    """

    cart_total = Decimal('0')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total


def cart_distinct_item_count(request):

    """
    renvoie le nombre total d'articles dans le panier de l'utilisateur
    """
    return get_cart_items(request).count()


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):

    """
    vide le panier d'achat du client actuel
    """
    user_cart = get_cart_items(request)
    user_cart.delete()


def remove_old_cart_items():

    """
    1. calculer la date d'il y a 90 jours (ou la durée de vie de la session)
    2. créer une liste des ID de chariot qui n'ont pas été modifiés
    3. supprimer ces instances CartItem
    """

    print("Enlever les anciennes commandes")
    remove_before = datetime.now() + timedelta(days=-settings.SESSION_COOKIE_DAYS)
    cart_ids = []
    old_items = CartItem.objects.values('cart_id').annotate(
        last_change=Max('date_added')).filter(last_change__lt=remove_before).order_by()

    for item in old_items:
        cart_ids.append(item['cart_id'])
    to_remove = CartItem.objects.filter(cart_id__in=cart_ids)
    to_remove.delete()
    print(str(len(cart_ids)) + " les anciennes ont été retirés")
