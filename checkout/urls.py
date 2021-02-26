# checkout.urls.py

from django.urls import path
from django.views.generic import TemplateView
from checkout.views import show_checkout, order_succes_view


app_name = 'checkout'
urlpatterns = [
    path('', show_checkout, name='checkout'),
    path('commande/success/', order_succes_view, name='order_success'),
]