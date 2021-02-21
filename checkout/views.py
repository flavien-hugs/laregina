# checkout.views.py

from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from core import settings
from cart import cart
from core import settings
from checkout import checkout
from checkout.models import Order
from checkout.forms import CheckoutForm


@login_required
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
            return HttpResponseRedirect(reverse('checkout:order_success'))
        else:
           messages.errors('Corrigez les erreurs ci-dessous')
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

    # context.update(csrf_token)
    return render(request, template, context)


class OrderResumeDetailView(TemplateView):
    """ 
    page affichée avec les informations relatives
    à la commande après qu'une commande ait été passée avec succès
    """
    template_name = 'checkout/snippet/_partials_order_success.html'
    extra_context = {'page_title': 'Résumé de votre commande'}

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Order.objects.filter(user=self.request.user)
        # kwargs['transaction_id'] = Order.objects.get(transaction_id=self.kwargs.transaction_id)
        print(kwargs['object_list'])
        return super().get_context_data(**kwargs)
