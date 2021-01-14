# catalogue.urls.py

from django.urls import path

from catalogue.views import ProductListView, ProductDetailView


app_name = 'catalogue'
urlpatterns = [
    path('tous-les-produits/', ProductListView.as_view(
        extra_context={'page_title': 'Tous les produits'}
    ), name='product_list'),
    path('detail/<slug>/', ProductDetailView.as_view(), name='product_detail'),
]