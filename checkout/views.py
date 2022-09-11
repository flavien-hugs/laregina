# checkout.views.py

from django.conf import settings
from django.template import Context
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from cart import cart
from checkout import checkout
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem

import io
import requests
from xhtml2pdf import pisa

from cinetpay_sdk.s_d_k import Cinetpay

apikey =  settings.CINETPAY_API_KEY
site_id =  settings.CINETPAY_SITE_ID

client = Cinetpay(apikey,site_id)


@csrf_exempt
def show_checkout(request, template='checkout/checkout.html'):

    if cart.is_empty(request):
        return HttpResponseRedirect(reverse('cart:cart'))

    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.process(request)
            order_id = response.get('order_id', 0)
            payment = response.get('payment')

            if payment == 0:
                if order_id:
                    request.session['order_id'] = str(order_id)

                    sucess_url = reverse(
                        'checkout:order_success',
                        kwargs={"order_id": order_id}
                    )
                return HttpResponseRedirect(sucess_url)

            if payment == 1:

                order = response.get('order')

                amount = order.get_order_total()
                transaction_id = order.transaction_id
                customer_name = order.get_short_name()

                NOTIFY_URL = "{% url  'cart:cart' %}"
                RETURN_URL = "{% url 'checkout:order_success' order_id=order.transaction_id %}"

                data = {
                    'amount' : amount,
                    'currency' : "XOF",
                    'transaction_id': transaction_id,
                    'description' : "Finaliser votre achat",
                    'return_url': RETURN_URL,
                    'customer_name' : customer_name,
                    'notify_url': NOTIFY_URL,
                    'customer_surname' : customer_name,
                }

                response = client.PaymentInitialization(data)

                PAYMENT_URL = response['data']['payment_url']
                return HttpResponseRedirect(PAYMENT_URL)
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
    }

    return render(request, template, context)


def order_success_view(
    request, order_id,
    template='checkout/checkout_success.html'
):

    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, transaction_id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    checkout.send_sms_order(order_id)
    checkout.send_sms_vendor(order_id)
    context = {
        'object': order,
        'order_items':order_items,
        'page_title': 'Commande validée'
    }

    return render(request, template, context)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    template_src = Context({'pagesize': 'A4'})
    html  = template.render(context_dict)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf',)
        response['Content-Disposition'] = 'attachment; filename="facture.pdf"'
        return response
    else:
        return HttpResponse("Erreur lors du rendu de la facture.", status=400)


def download_invoice_view(request, order_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    mydict = {
        'object_date': order.date,
        'order_total': order.get_order_total,
        'object_id': order.transaction_id,
        'get_full_name': order.get_full_name,
        'get_shipping_delivery': order.get_shipping_delivery,
        'order_item': order_item,
    }
    return render_to_pdf('checkout/snippet/_partials_order_invoice.html', mydict)


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
