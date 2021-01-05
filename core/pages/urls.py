# static pages url


from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns  = [

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

    path('about-us/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'À propos de nous', 'page_description': "Qui sommes-nous ?"
        }, template_name='pages/about-us.html')), name='about-us'),
    path('faqs/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'Faqs : Questions fréquemment posées', 'page_description': "Questions fréquemment posées"
        }, template_name='pages/faqs.html')), name='faqs'),
    path('contact/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'Nous contacter', 'page_description': "Contactez-nous pour toute question"
        }, template_name='pages/contact.html')), name='contact'),
    
    path('vendor/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'Tableau de bord', 'page_description': "Tableau de bord"
        }, template_name='seller_dashboard/index.html')), name='vendor-admin'),
    path('product/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'Liste des produits', 'page_description': "Liste des produits"
        }, template_name='seller_dashboard/layouts/product.html')), name='vendor-product'),
    path('product/add/', TemplateView.as_view(
        extra_context={'page_title': 'Ajouter un produit', 'page_description': "Ajouter un produit"
        }, template_name='seller_dashboard/layouts/add_product.html'), name='vendor-product-add'),
    path('orders/', TemplateView.as_view(
        extra_context={'page_title': 'Liste des commandes', 'page_description': "Liste des commandes"
        }, template_name='seller_dashboard/layouts/orders.html'), name='vendor-orders'),
    path('orders/detail/', TemplateView.as_view(
        extra_context={'page_title': 'Detail de la commande', 'page_description': "Detail de la commande"
        }, template_name='seller_dashboard/layouts/orders_detail.html'), name='vendor-order-detail'),
    path('orders/settings/', TemplateView.as_view(
        extra_context={'page_title': 'Configuration', 'page_description': "Configuration"
        }, template_name='seller_dashboard/layouts/settings-store.html'), name='vendor-settings'),
    path('store/', TemplateView.as_view(
        extra_context={'page_title': 'Vendor store', 'page_description': "Vendor store"
        }, template_name='seller_dashboard/layouts/vendor-store.html'), name='vendor-store'),
]
