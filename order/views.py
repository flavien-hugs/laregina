# order.views.py

from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from cart import cart
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
            response = checkout.process(request)            
            order_number = response.get('order_number', 0)
            message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                return HttpResponseRedirect(reverse('order:checkout_receipt'))
        else:
            message = messages.info('Corrigez les erreurs ci-dessous')
    else:
        if request.user.is_authenticated:
            # user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=request.user)
        else:
            form = CheckoutForm()

    context = {
        'page_title': 'Checkout',
        'form': form,
        'cart_items': cart.get_cart_items(request),
        'cart_subtotal': cart.cart_subtotal(request)
    }

    # context.update(csrf_token)
    return render(request, template, context)


def receipt(request, template='checkout/receipt.html'):
    
    """ 
    page affichée avec les informations relatives
    à la commande après qu'une commande ait été passée avec succès
    """

    order_number = request.session.get('order_number', '')
    
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
    else:
        return HttpResponseRedirect(reverse('cart:cart'))
    
    context = {
        'order': order,
        'order_items': order_items,
        'order_number': order_number
    }

    return render(request, template, context)
