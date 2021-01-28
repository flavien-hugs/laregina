# reviews.urls.py

from django.urls import path
from catalogue.views import addRreview

app_name = 'reviews'
urlpatterns = [
    path('add/<slug>/', addRreview, name='add_product_review'),
]
