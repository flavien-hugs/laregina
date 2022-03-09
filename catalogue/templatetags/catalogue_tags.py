# catalogue filters

import locale
import random
from itertools import chain

from django import template
from django.contrib.auth import get_user_model

from cart import cart
from catalogue.models import Product
from pages.models import Campaign, Promotion

register = template.Library()


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


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


@register.inclusion_tag("includes/partials/_partials_hero_slider.html")
def hero_slider_list(count=5):
    promotions = Promotion.objects.all()[:count]
    object_list = sorted(chain(promotions), key=lambda x: random.random())
    context = {'object_list': object_list}
    return context

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


@register.inclusion_tag("includes/partials/_partials_product_recent.html")
def product_recent_list(count=80):
    product_list = sorted(Product.objects.product_recent()[:count], key=lambda x: random.random())
    context = {'object_product_recent': product_list}
    return context


@register.inclusion_tag("includes/partials/_partials_products_selling.html")
def best_selling_products(count=20):
    products = Product.objects.all()
    products_selling = sorted(products[:count], key=lambda x: random.random())
    context = {
        'header_text': "Les plus vendus",
        'selling_products': products_selling
    }
    return context


@register.inclusion_tag("includes/partials/_partials_sales_flash.html")
def product_sales_flash(count=20):
    products = Product.objects.all()
    sales_flash = sorted(
        Campaign.objects.ventes_flash()[:count],
        key=lambda x: random.random()
    )
    context = {
        'header_text': "Ventes Flash",
        'object_promotion_list': sales_flash
    }
    return context

@register.inclusion_tag("includes/partials/_partials_sales_flash.html")
def product_destockages(count=20):
    products = Product.objects.all()
    destockages = sorted(
        Campaign.objects.destockages()[:count],
        key=lambda x: random.random()
    )
    context = {
        'header_text': "Déstockages",
        'object_promotion_list': destockages
    }
    return context


@register.inclusion_tag("includes/partials/_partials_sales_flash.html")
def product_nouvelle_arrivages(count=20):
    products = Product.objects.all()
    nouvelle_arrivages = sorted(
        Campaign.objects.nouvelle_arrivages()[:count],
        key=lambda x: random.random()
    )
    context = {
        'header_text': "Nouveautés",
        'object_promotion_list': nouvelle_arrivages
    }
    return context

@register.inclusion_tag("includes/partials/_partials_vendors.html")
def vendor_recent(count=50):
    vendor_list = get_user_model().objects.order_by('-date_joined')[:count]
    context = {'object_vendor_recent': vendor_list}
    return context
