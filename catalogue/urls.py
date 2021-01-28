# catalogue.urls.py

from django.urls import path

from catalogue.views import ProductListView, show_product

app_name = 'catalogue'
urlpatterns = [
    path('tous-les-produits/', ProductListView.as_view(), name='product_list'),
    path('detail/<slug>/', show_product, name='product_detail'),
]