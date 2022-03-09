# accounts/urls.py

from django.urls import path, include
from django.views.generic import TemplateView

from pages import views
from accounts.views import customer, seller


urlpatterns = [
    path('customer/', include(([
        path(route='dashboard/', view=TemplateView.as_view(
            template_name='dashboard/customer/index.html'
        ), name='customer_dashboard'),
    ], 'accounts'), namespace='customer')),

    path('dashboard/seller/0/me/', include(([
        path(route='', view=seller.dashboard_view, name='profile'),

        path(route='commande/', view=seller.order_list_view, name='order_list'),
        path(route='commande/<pk>/detail/', view=seller.order_detail_view, name='order_detail'),

        path(route='produit/', view=seller.product_list_view, name='product_list'),
        path(route='produit/add/', view=seller.product_create_view, name='product_create'),
        path(route='produit/<slug>/update/', view=seller.product_update_view, name='product_update'),
        path(route='produit/<slug>/delete/',view=seller.product_delete_view, name='product_delete'),

        path(route='parametre/<slug>/update/', view=seller.settings_view, name='update'),
        path(route='parametre/<slug>/social/update/', view=seller.social_media_view, name='rs_update'),

        path(route='promotion/', view=views.promotion_list, name='promotion_list'),
        path(route='promotion/add/', view=views.promotion_view, name='promotion_create'),
        path(route='promotion/<slug>/update/', view=views.promotion_update, name='promotion_update'),
        path(route='promotion/<slug>/delete/', view=views.promotion_delete, name='promotion_delete'),
    ], 'accounts'), namespace='seller')),

    path('boutique/', include(([
        path(route='all/', view=seller.store_list_view, name='store_list_view'),
        path(route='<slug>/detail/', view=seller.store_detail_view, name='store_detail_view'),
    ], 'accounts'), namespace='vendor')),
]