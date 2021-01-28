# static pages url


from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from accounts.views import seller

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns  = [
    path('payment/', TemplateView.as_view(
        extra_context={'page_title': 'Payment', 'page_description': "Payment"
        }, template_name='payment/payment.html'), name='payment'),
    path('payment-success/', TemplateView.as_view(
        extra_context={'page_title': 'Paiement réussi', 'page_description': "Paiement réussi"
        }, template_name='payment/payment-success.html'), name='payment-success'),
    
    # static page urls
    path('tracking-order/', TemplateView.as_view(
        extra_context={'page_title': 'Suivi de commande', 'page_description': "Suivi de commande"
        }, template_name='pages/tracking-order.html'), name='tracking-order'),


    path('product/', cache_page(CACHE_TTL)(TemplateView.as_view(
        extra_context={'page_title': 'Liste des produits', 'page_description': "Liste des produits"
        }, template_name='dashboard/seller/layouts/product.html')), name='vendor-product'),
    path('product/add/', TemplateView.as_view(
        extra_context={'page_title': 'Ajouter un produit', 'page_description': "Ajouter un produit"
        }, template_name='dashboard/seller/layouts/add_product.html'), name='vendor-product-add'),
    path('orders/', TemplateView.as_view(
        extra_context={'page_title': 'Liste des commandes', 'page_description': "Liste des commandes"
        }, template_name='dashboard/seller/layouts/orders.html'), name='vendor-orders'),
    path('orders/detail/', TemplateView.as_view(
        extra_context={'page_title': 'Detail de la commande', 'page_description': "Detail de la commande"
        }, template_name='dashboard/seller/layouts/orders_detail.html'), name='vendor-order-detail'),

    path('magasin/<slug>/', seller.StoreDetailView.as_view(), name='store_detail_view'),
]
