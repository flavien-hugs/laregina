# checkout.urls.py

from django.urls import path
from django.views.generic import TemplateView

from checkout import views


app_name = 'checkout'
urlpatterns = [
    path('', views.show_checkout, name='checkout'),
    path('commande/success/', views.order_success_view, name='order_success'),
]