# order.urls.py

from django.urls import path
from order.views import show_checkout, receipt

app_name = 'order'
urlpatterns = [
    path('', show_checkout, name='checkout'),
    path('receipt/', receipt, name='checkout_receipt'),
]