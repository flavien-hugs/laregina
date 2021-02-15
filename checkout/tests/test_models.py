# checkout.tests.test_models.py

import http.client
from django.urls import reverse, resolve
from django.test import TestCase, Client

from cart import cart
from cart.models import CartItem
from catalogue.models import Product
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem


class CheckoutTestCase(TestCase):
    
    """
    teste la fonctionnalité de la page du formulaire de paiement
    """
    
    def setUp(self):
        self.client = Client()
        home_url = reverse('home')
        self.checkout_url = reverse('checkout:checkout')
        self.client.get(home_url)
        
        # nécessite de créer d'abord un client avec un panier d'achat
        # self.item = CartItem.objects.create(
        #     cart_id=self.client.session[cart.CART_ID_SESSION_KEY],
        #     quantity=1,
        #     product=Product.objects.all()
        # )
        # self.item.save()

    def test_checkout_page_empty_cart(self):

        """
        le panier vide doit être redirigé vers
        la page du panier
        """
        
        client = Client()
        cart_url = reverse('cart:cart')
        response = client.get(self.checkout_url)
        self.assertRedirects(response, cart_url)


    def test_checkout_page(self):
        
        # avec au moins un article dans le panier,
        # la demande d'URL de la page de paiement est acceptée

        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "checkout")
        
        url_entry = resolve(self.checkout_url)
        template_name = url_entry[2]['template_name']
        self.assertTemplateUsed(response, template_name)


    """ def test_submit_empty_form(self):
        
        un formulaire de commande vide donne lieu à un message d'erreur
        "obligatoire" pour les champs obligatoires du formulaire de commande
        

        form = CheckoutForm()
        response = self.client.post(self.checkout_url, form.initial)
        for name, field in form.fields.iteritems():
            value = form.fields[name]
            if not value and form.fields[name].required:
                error_msg = form.fields[name].error_messages['required']
                self.assertFormError(response, "form", name, [error_msg])"""