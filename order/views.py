# order.views.py

from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cart import cart
from core import settings
from order import checkout
from accounts import profile
from order.forms import CheckoutForm
from order.models import Order, OrderItem


def show_checkout(request, template='checkout/checkout.html'):
    
    """
    checkout form page to collect user shipping and billing information
    """
    
    if cart.is_empty(request):
        return HttpResponseRedirect(reverse('cart:cart'))
    
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            checkout.create_order(request)
            return HttpResponseRedirect(reverse('order:checkout_receipt'))
        else:
            message = messages.danger('Corrigez les erreurs ci-dessous')
    else:
        if request.user.is_authenticated:
            # user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=request.user)
        else:
            form = CheckoutForm()

    context = {
        'form': form,
        'page_title': 'Checkout',
        'cart_items': cart.get_cart_items(request),
        'cart_subtotal': cart.cart_subtotal(request),
        'APIKEY': settings.CINETPAY_API_KEY,
        'SITEID': settings.CINETPAY_SITE_ID,
        'TRANSID': settings.CINETPAY_TRANS_ID
    }

    # context.update(csrf_token)
    return render(request, template, context)


def receipt(request, template='checkout/receipt.html'):
    
    """ 
    page affichée avec les informations relatives
    à la commande après qu'une commande ait été passée avec succès
    """

    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders,
    }

    return render(request, template, context)
