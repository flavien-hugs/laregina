# catalogue.urls.py

from django.urls import path

from catalogue import views


app_name = 'catalogue'
urlpatterns = [
    path('tous-les-produits/', views.ProductListView.as_view(), name='product_list'),
    path('detail/<slug>/', views.show_product, name='product_detail'),
]
