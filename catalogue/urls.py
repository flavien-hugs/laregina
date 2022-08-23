# catalogue.urls.py

from django.urls import path, include

from pages import views as pages_views
from catalogue import views as catalogue_views


urlpatterns = [
    path('', include(([
        path(route='produit/', view=catalogue_views.product_list_view, name='product_list'),
        path(route='ps-<slug>/', view=catalogue_views.show_product, name='product_detail'),
    ], 'catalogue'), namespace='catalogue')),

    path('promotion/', include(([
        path(route='<slug>/', view=pages_views.promotion_detail, name='promotion_detail'),
        path(route='destockages/list/', view=pages_views.destockage_list_view, name='promotion_destockage_list'),
        path(route='flash-sales/list/', view=pages_views.sales_flash_list_view, name='promotion_sales_flash_list'),
        path(route='nouveautes/list/', view=pages_views.news_arrivals_list_view, name='promotion_news_arrival_list'),
    ], 'catalogue'), namespace='promotion')),
]
