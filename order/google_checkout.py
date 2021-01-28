# order.google_checkout.py

import json
import base64
import http.client
from xml.dom import minidom
from xml.dom.minidom import Document
from django.http import HttpRequest, HttpResponseRedirect

from cart import cart
from core import settings
from cart.models import CartItem



def get_checkout_url(request):

    """
    fait une demande à Google Checkout avec un panier XML et analyse l'URL
    de la caisse retournée à laquelle nous envoyons le client lorsqu'il
    est prêt à passer à la caisse.
    """
    redirect_url = ''
    req = _create_google_checkout_request(request)
    try:
        response_xml = urllib.request.urlopen(req)
    except HTTPError as err:
        raise err
    except URLError as err:
        raise err
    else:
        redirect_url = _parse_google_checkout_response(response_xml)
    return redirect_url


def _create_google_checkout_request(request):

    """
    construit une requête de réseau contenant une version XML
    du contenu du panier d'un client pour la soumettre à Google Checkout 
    """

    url = settings.GOOGLE_CHECKOUT_URL
    cart = _build_xml_shopping_cart(request)
    # json_data = json.dumps(cart)
    req = http.client.HTTPSConnection(url)
    req.request("POST", data=cart)
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID
    merchant_key = settings.GOOGLE_CHECKOUT_MERCHANT_KEY
    key_id = merchant_id + ':' + merchant_key
    authorization_value = base64.encodestring(key_id)[:-1]
    req.add_header('Authorization', 'Basic %s' % authorization_value)
    req.add_header('Content-Type', 'application/xml; charset=UTF-8')
    req.add_header('Accept', 'application/xml; charset=UTF-8')
    
    return req

def _parse_google_checkout_response(response_xml):

    """
    obtenir la réponse XML d'un POSTE XML à Google Vérifier les articles de notre panier
    """
    
    redirect_url = ''
    xml_doc = minidom.parseString(response_xml)
    root = xml_doc.documentElement
    node = root.childNodes[1]
    if node.tagName == 'redirect-url':
        redirect_url = node.firstChild.data
    if node.tagName == 'error-message':
        raise RuntimeError(node.firstChild.data)
    return redirect_url
    
    
def _build_xml_shopping_cart(request):
    
    """
    construit la représentation XML des articles du panier
    d'achat du client actuel pour POSTER à l'API Google Checkout
    """

    doc = Document()
    root = doc.createElement('checkout-shopping-cart')
    root.setAttribute('xmlns', 'http://checkout.google.com/schema/2')
    doc.appendChild(root)
    shopping_cart = doc.createElement('shopping-cart')
    root.appendChild(shopping_cart)
    items = doc.createElement('items')
    shopping_cart.appendChild(items)
    cart_items = cart.get_cart_items(request)
    
    for cart_item in cart_items:
        item = doc.createElement('item')
        items.appendChild(item)
        
        item_name = doc.createElement('item-name')
        item_name_text = doc.createTextNode(str(cart_item.name))
        item_name.appendChild(item_name_text)
        item.appendChild(item_name)
        
        item_description = doc.createElement('item-description')
        item_description_text = doc.createTextNode(str(cart_item.name))
        item_description.appendChild(item_description_text)
        item.appendChild(item_description)
        
        unit_price = doc.createElement('unit-price')
        unit_price.setAttribute('currency','USD')
        unit_price_text = doc.createTextNode(str(cart_item.price))
        unit_price.appendChild(unit_price_text)
        item.appendChild(unit_price)
        
        quantity = doc.createElement('quantity')
        quantity_text = doc.createTextNode(str(cart_item.quantity))
        quantity.appendChild(quantity_text)
        item.appendChild(quantity)
        
    checkout_flow = doc.createElement('checkout-flow-support')
    root.appendChild(checkout_flow)
    merchant_flow = doc.createElement('merchant-checkout-flow-support')
    checkout_flow.appendChild(merchant_flow)
    
    shipping_methods = doc.createElement('shipping-methods')
    merchant_flow.appendChild(shipping_methods)
    
    flat_rate_shipping = doc.createElement('flat-rate-shipping')
    flat_rate_shipping.setAttribute('name','FedEx Ground')
    shipping_methods.appendChild(flat_rate_shipping)
    
    shipping_price = doc.createElement('price')
    shipping_price.setAttribute('currency','EURO')
    flat_rate_shipping.appendChild(shipping_price)
    
    shipping_price_text = doc.createTextNode('9.99')
    shipping_price.appendChild(shipping_price_text)
    
    return doc.toxml(encoding='utf-8')
