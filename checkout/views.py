# checkout.views.py

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from cart import cart
from core import settings
from checkout import checkout
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem


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
            order_id = response.get('order_id', 0)
            print(order_id)
            if order_id:
                request.session['order_id'] = order_id
                sucess_url = reverse('checkout:order_success') 
            return HttpResponseRedirect(sucess_url)
    else:
        if request.user.is_authenticated:
            form = CheckoutForm(instance=request.user)
        else:
            form = CheckoutForm()

    context = {
        'form': form,
        'page_title': 'Paiement',
        'cart_items': cart.get_cart_items(request),
        'cart_subtotal': cart.cart_subtotal(request),
        'APIKEY': settings.CINETPAY_API_KEY,
        'SITEID': settings.CINETPAY_SITE_ID,
    }

    return render(request, template, context)


def order_succes_view(request, template='checkout/checkout_success.html'):

    order_id = request.session.get('order_id', '')

    if order_id:
        order = Order.objects.filter(transaction_id=order_id)[0]
        order_items = OrderItem.objects.filter(order=order)
    else:
        cart_url = reverse('cart:cart')
        return HttpResponseRedirect(cart_url)
    
    context = {
        'page_title': 'Commande validée',
        'object': Order.objects.filter(transaction_id=order_id)[0],
        'order_items': OrderItem.objects.filter(order=order)
    }

    return render(request, template, context)


def order_succes_view(request, template='checkout/checkout_success.html'):

    order_id = request.session.get('order_id', '')

    if order_id:
        order = Order.objects.filter(transaction_id=order_id)[0]
        order_items = OrderItem.objects.filter(order=order)
    else:
        cart_url = reverse('cart:cart')
        return HttpResponseRedirect(cart_url)
    
    context = {
        'page_title': 'Commande validée',
        'object': Order.objects.filter(transaction_id=order_id)[0],
        'order_items': OrderItem.objects.filter(order=order)
    }

    return render(request, template, context)


class TrackOrderView(ListView):
    template_name = 'checkout/snippet/_partials_order_tracking.html'
    success_url = reverse_lazy('order_tracking')

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.request.GET.get('track', None)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        query = self.request.GET.get('track', None)
        if query is not None:
            return Order.objects.track_order(query)
        return Order.objects.none()
