from analytics import utils
from cart import cart
from checkout import checkout
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def shopcart(request, template="cart/cart.html"):
    request.session.set_expiry(settings.CACHE_TTL)

    if request.method == "POST":
        postdata = request.POST.copy()

        if postdata["submit"] == "remove":
            cart.remove_from_cart(request)
            messages.success(request, "L'article a été retiré de votre panier.")

        if postdata["submit"] == "update":
            cart.update_cart(request)
            messages.success(request, "Super ! Vous avez mis votre panier à jour.")

        if postdata["submit"] == "checkout":
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)

    context = {
        "page_title": "Panier",
        "cart_items": cart.get_cart_items(request),
        "cart_subtotal": cart.cart_subtotal(request),
        "recently_viewed": utils.get_recently_viewed(request),
    }

    return render(request, template, context)


shopcart = shopcart
