# static pages url

from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page


urlpatterns  = [
    path('account/seller/register/', TemplateView.as_view(
        extra_context={'page_title': 'Créer un compte', 'page_description': "Ouvrir ma boutique"
        }, template_name='accounts/register.html'), name='register'),
    path('account/seller/connexion/', TemplateView.as_view(
        extra_context={'page_title': 'Se connecter', 'page_description': "Connectez-vous à votre compte"
        }, template_name='accounts/login.html'), name='login'),

    path('list/', TemplateView.as_view(
        extra_context={'page_title': 'Liste des produits', 'page_description': "Tous les produits des magasins"
        }, template_name='catalogue/list.html'), name='list'),
    path('detail/', TemplateView.as_view(
        extra_context={'page_title': 'Detail du produit', 'page_description': "Detail du produit"
        }, template_name='catalogue/detail.html'), name='detail'),

    path('panier/', TemplateView.as_view(
        extra_context={'page_title': 'Panier', 'page_description': "Detail du panier"
        }, template_name='cart/cart.html'), name='cart'),
    path('checkout/', TemplateView.as_view(
        extra_context={'page_title': 'Checkout', 'page_description': "Checkout"
        }, template_name='checkout/checkout.html'), name='checkout'),
    path('payment/', TemplateView.as_view(
        extra_context={'page_title': 'Payment', 'page_description': "Payment"
        }, template_name='payment/payment.html'), name='payment'),
    path('payment-success/', TemplateView.as_view(
        extra_context={'page_title': 'Paiement réussi', 'page_description': "Paiement réussi"
        }, template_name='payment/payment-success.html'), name='payment-success'),
    path('tracking-order/', TemplateView.as_view(
        extra_context={'page_title': 'Suivi de commande', 'page_description': "Suivi de commande"
        }, template_name='pages/tracking-order.html'), name='tracking-order'),

    path('about-us/', cache_page(60 * 2)(TemplateView.as_view(
        extra_context={'page_title': 'À propos de nous', 'page_description': "Qui sommes-nous ?"
        }, template_name='pages/about-us.html')), name='about-us'),
    path('faqs/', cache_page(60 * 2)(TemplateView.as_view(
        extra_context={'page_title': 'Faqs : Questions fréquemment posées', 'page_description': "Questions fréquemment posées"
        }, template_name='pages/faqs.html')), name='faqs'),
    path('contact/', cache_page(60 * 2)(TemplateView.as_view(
        extra_context={'page_title': 'Nous contacter', 'page_description': "Contactez-nous pour toute question"
        }, template_name='pages/contact.html')), name='contact'),
]
