# cart.views.py

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from cart import cart
from core import settings
from order import checkout

from analytics.utils import(
    get_recently_viewed,
    recommended_from_views,
    recommended_from_search
)


def shopcart(request, template="cart/cart.html"):

    request.session.set_expiry(120000)

    if request.method == 'POST':
        postdata = request.POST.copy()

        if postdata['submit'] == 'remove':
            cart.remove_from_cart(request)
            messages.success(request, "L'article a été retiré de votre panier.")

        if postdata['submit'] == 'update':
            cart.update_cart(request)
            messages.success(request, "Super ! Vous avez mis votre panier à jour.")

        if postdata['submit'] == 'checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)

    context = {
        'page_title': 'Panier',
        'cart_items': cart.get_cart_items(request),
        'cart_subtotal': cart.cart_subtotal(request),
        'recently_viewed': get_recently_viewed(request),
        'recommended_product': recommended_from_views(request),
    }

    return render(request, template, context)
