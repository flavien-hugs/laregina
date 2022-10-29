# accounts/urls.py

from django.urls import path, include
from django.views.generic import TemplateView

from pages import views
from accounts.views import customer, seller


urlpatterns = [
    path('dashboard/seller/0/me/', include(([
        path(
            route='',
            view=seller.dashboard_view,
            name='profile'
        ),
        path(
            route='commande/index/',
            view=seller.order_list_view,
            name='order_list'
        ),
        path(
            route='commande/<int:pk>/detail/',
            view=seller.order_detail_view,
            name='order_detail'
        ),

        path(
            route='produit/index/',
            view=seller.product_list_view,
            name='product_list'
        ),
        path(
            route='produit/create/',
            view=seller.product_create_view,
            name='product_create'
        ),
        path(
            route='produit/<str:slug>/update/',
            view=seller.product_update_view,
            name='product_update'
        ),
        path(
            route='produit/<str:slug>/delete/',
            view=seller.product_delete_view,
            name='product_delete'
        ),

        path(
            route='parametre/<str:slug>/update/',
            view=seller.settings_view,
            name='update'
        ),
        path(
            route='parametre/<str:slug>/social/update/',
            view=seller.social_media_view,
            name='rs_update'
        ),

        path(
            route='reduction/create/',
            view=seller.voucher_create_view,
            name='voucher_create'
        ),
        path(
            route='reduction/<int:pk>/update/',
            view=seller.voucher_update_view,
            name='voucher_update'
        ),
        path(
            route='reduction/<int:pk>/delete/',
            view=seller.voucher_delete_view,
            name='voucher_delete'
        ),
        path(
            route='reduction/index/',
            view=seller.voucher_list_view,
            name='voucher_list'
        ),

        path(
            route='promotion/index/',
            view=views.promotion_list,
            name='promotion_list'
        ),
        path(
            route='promotion/create/',
            view=views.promotion_view,
            name='promotion_create'
        ),
        path(
            route='promotion/<str:slug>/update/',
            view=views.promotion_update,
            name='promotion_update'
        ),
        path(
            route='promotion/<str:slug>/delete/',
            view=views.promotion_delete,
            name='promotion_delete'
        ),
    ], 'accounts'), namespace='seller')),

    path('customer/', include(([
        path(
            route='dashboard/',
            view=TemplateView.as_view(template_name='dashboard/customer/index.html'),
            name='customer_dashboard'),
    ], 'accounts'), namespace='customer')),

    path('marketplace/', include(([
        path(
            route='',
            view=seller.store_list_view,
            name='store_list_view'
        ),
        path(
            route='<str:slug>/',
            view=seller.store_detail_view,
            name='store_detail_view'
        ),
    ], 'accounts'), namespace='vendor')),
]
