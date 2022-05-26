# checkout.urls.py

from django.urls import path
from django.views.generic import TemplateView

from checkout import views


app_name = 'checkout'
urlpatterns = [
    path(
        route='',
        view=views.show_checkout,
        name='checkout'
    ),
    path(
        route='commande/success/<order_id>',
        view=views.order_success_view,
        name='order_success'
    ),
]
