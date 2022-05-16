# cart.cart.py

import random
import string
from decimal import Decimal
from django.db.models import Max
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from helpers.utils import generate_key

from cart.models import CartItem
from catalogue.models import Product


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):

    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():

    cart_id = ''
    characters = string.ascii_letters + string.ascii_lowercase + string.digits
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


def get_cart_items(request):

    return CartItem.objects.filter(cart_id=_cart_id(request),)


def add_to_cart(request):

    postdata = request.POST.copy()

    slug = postdata.get('slug', '')

    quantity = postdata.get('quantity', 1)

    p = get_object_or_404(Product, slug=slug)

    cart_products = get_cart_items(request)
    product_in_cart = False

    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def update_cart(request):
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

    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):

    cart_total = Decimal('0')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.get_product_price() * cart_item.quantity
    return int(cart_total)


def cart_distinct_item_count(request):
    return get_cart_items(request).count()


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):

    user_cart = get_cart_items(request)
    user_cart.delete()


def remove_old_cart_items():

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
