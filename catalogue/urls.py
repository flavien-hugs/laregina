# catalogue.urls.py

from django.urls import path, include

from pages import views as pages_views
from catalogue import views as catalogue_views


urlpatterns = [
    path('', include(([
        path(route='produit/', view=catalogue_views.ProductListView.as_view(), name='product_list'),
        path(route='ps-<slug>/', view=catalogue_views.show_product, name='product_detail'),
    ], 'catalogue'), namespace='catalogue')),

    path('prm-', include(([
        path(route='<slug>/', view=pages_views.promotion_detail, name='promotion_detail'),
    ], 'catalogue'), namespace='promotion')),
]
