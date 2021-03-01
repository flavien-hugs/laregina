# catalogue filters

import locale
from django import template

from cart import cart

register = template.Library()


# afficher la monnaie
@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_MONETARY, 'fr_Fr.UTF-8')
    except:
        locale.setlocale(locale.LC_MONETARY, '')
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)


# compter le nombre d'articles dans le panier
@register.simple_tag
def cart_items_count(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return cart_item_count

# article dans le panier
@register.simple_tag
def items(request):
    item_in_cart = cart.get_cart_items(request)
    return item_in_cart

# lister les articles dans le panier
@register.inclusion_tag('cart/snippet/_snippet_cart_items.html')
def shopcart_items(items, request):
    return {
        'items': cart.get_cart_items(request),
        'cart_subtotal': cart.cart_subtotal(request)
    }

@register.inclusion_tag("includes/partials/_partials_product_list.html")
def product_list(object_list, header_text):
    return {
        'object_list': object_list,
        'header_text': header_text
    }
