# accounts/urls.py

from django.urls import path, include
from django.views.generic import TemplateView

from pages import views
from accounts.views import auth_views, seller_views


urlpatterns = [

    path('sp-marketplace-vendeurs/', include(([
        path(route='inscription/',
            view=auth_views.seller_signup_view,
            name='account_signup'),

        path(route='connexion/',
            view=auth_views.user_login_view,
            name='account_login'),

        path(route='reset-password/',
            view=auth_views.account_request_password_reset_view,
            name='account_reset_password'
        ),

        path(route='reset-password/<uidb64>/<token>/',
            view=auth_views.account_request_password_reset_view,
            name='account_reset_password'
        ),

        path(
            route='set-new-password/<uidb64>/<token>/',
            view=auth_views.account_set_new_password_view,
            name='set_new_password'
        ),

        path(route='logout/',
            view=auth_views.logout_view,
            name='account_logout'),
    ], 'accounts'), namespace='auth_views')),

    path('dashboard/seller/0/me/', include(([
        path(
            route='',
            view=seller_views.dashboard_view,
            name='profile'
        ),
        path(
            route='commande/index/',
            view=seller_views.order_list_view,
            name='order_list'
        ),
        path(
            route='commande/<int:pk>/detail/',
            view=seller_views.order_detail_view,
            name='order_detail'
        ),

        path(
            route='produit/index/',
            view=seller_views.product_list_view,
            name='product_list'
        ),
        path(
            route='produit/create/',
            view=seller_views.product_create_view,
            name='product_create'
        ),
        path(
            route='produit/<str:slug>/update/',
            view=seller_views.product_update_view,
            name='product_update'
        ),
        path(
            route='produit/<str:slug>/delete/',
            view=seller_views.product_delete_view,
            name='product_delete'
        ),

        path(
            route='parametre/<str:slug>/update/',
            view=seller_views.settings_view,
            name='update'
        ),
        path(
            route='parametre/<str:slug>/social/update/',
            view=seller_views.social_media_view,
            name='rs_update'
        ),

        path(
            route='reduction/create/',
            view=seller_views.voucher_create_view,
            name='voucher_create'
        ),
        path(
            route='reduction/<int:pk>/update/',
            view=seller_views.voucher_update_view,
            name='voucher_update'
        ),
        path(
            route='reduction/<int:pk>/delete/',
            view=seller_views.voucher_delete_view,
            name='voucher_delete'
        ),
        path(
            route='reduction/index/',
            view=seller_views.voucher_list_view,
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
    ], 'accounts'), namespace='dashboard_seller')),

    path('marketplace/', include(([
        path(
            route='',
            view=seller_views.store_list_view,
            name='store_list_view'
        ),
        path(
            route='<str:slug>/',
            view=seller_views.store_detail_view,
            name='store_detail_view'
        ),
    ], 'accounts'), namespace='vendor')),
]
