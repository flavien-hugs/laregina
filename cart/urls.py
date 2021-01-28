# cart.urls.py

from django.urls import path
from cart.views import shopcart

app_name = 'cart'
urlpatterns = [
    path('', shopcart, name='cart'),
]
