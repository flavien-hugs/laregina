# checkout.urls.py

from django.urls import path
from django.views.generic import TemplateView
from checkout.views import show_checkout, OrderResumeDetailView


app_name = 'checkout'
urlpatterns = [
    path('', show_checkout, name='checkout'),
    path('resume/<pk>/', OrderResumeDetailView.as_view(), name='checkout_receipt'),
    path('order/success/', OrderResumeDetailView.as_view(
        extra_context={'page_title': 'Commande réussie',
        'page_description': "Super, votre commande a été enregistrée."
    }), name='order_success'),

    path('tracking/order/', TemplateView.as_view(
        extra_context={'page_title': 'Suivi votre commande', 'page_description': "Suivi de commande"
        }, template_name='checkout/snippet/_partials_order_tracking.html'), name='order_tracking'),
]