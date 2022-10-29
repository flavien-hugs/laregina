# catalogue.urls.py

from django.urls import path, include

from pages import views as pages_views

from cart.views import shopcart
from catalogue import views as catalogue_views
from category.views import category_detail_view


urlpatterns = [
    path(route='',
        view=catalogue_views.combine_view,
        name='home'
    ),

    path('cart/index/', include(([
        path(route="", view=shopcart, name='cart'),
    ], 'catalogue'), 'cart')),

    path('', include(([
        path(route='produit/',
            view=catalogue_views.product_list_view,
            name='product_list'),
        path(route='ps-<str:slug>-<int:pk>/',
            view=catalogue_views.show_product,
            name='product_detail'),
    ], 'catalogue'), namespace='catalogue')),

    path('', include(([
        path(route='<str:slug>/',
            view=category_detail_view,
            name='category_detail'),
    ], 'catalogue'), 'category')),

    path('avis-cliens/', include(([
        path(route='<str:slug>/',
            view=catalogue_views.add_review,
            name='add_product_review'),
    ], 'catalogue'), namespace='reviews')),

    path('promotion/', include(([
        path(route='<str:slug>/',
            view=pages_views.promotion_detail,
            name='promotion_detail'),
        path(route='destockages/list/',
            view=pages_views.destockage_list_view,
            name='promotion_destockage_list'),
        path(route='flash-sales/list/',
            view=pages_views.sales_flash_list_view,
            name='promotion_sales_flash_list'),
        path(route='nouveautes/list/',
            view=pages_views.news_arrivals_list_view,
            name='promotion_news_arrival_list'),
    ], 'catalogue'), namespace='promotion'))
]
