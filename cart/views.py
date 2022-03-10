# cart.views.py

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from cart import cart
from core import settings
from checkout import checkout
from pages.models import Campaign

from analytics.utils import get_recently_viewed, recommended_from_views


@csrf_exempt
def shopcart(request, template="cart/cart.html"):

    request.session.set_expiry(12000)

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
        'destockages': Campaign.objects.destockages()[:15],
        'sales_flash': Campaign.objects.ventes_flash()[:15],
        'news_arrivals': Campaign.objects.nouvelle_arrivages()[:15]
    }

    return render(request, template, context)
