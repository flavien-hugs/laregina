# accounts/urls.py

from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import customer, seller


urlpatterns = [
    path('customer/', include(([
        path('dashboard/', TemplateView.as_view(
            template_name='dashboard/customer/index.html'
        ), name='customer_dashboard'),
    ], 'accounts'), namespace='customer')),

    path('seller/', include(([
        path('dashboard/', seller.DashboardView.as_view(
            extra_context={'page_description': "Tableau de bord"}
        ), name='profile'),

        path('commande/', seller.OrderListView.as_view(
            extra_context={
                'page_title': 'Liste des vos commandes',
                'page_description': "Liste des commandes"
            }
        ), name='order_list'),

        path('commande/detail/<pk>/', seller.OrderDetailView.as_view(
            extra_context={
                'page_description': "Detail de la commande"
            }, template_name='dashboard/seller/includes/_partials_orders_detail.html'
        ), name='order_detail'),

        path('product/list/', seller.ProductListView.as_view(
            extra_context={
                'page_title': 'Liste de vos produit en vente',
                'page_description': "Liste des produits"
            },
        ), name='product_list'),

        path('create/product/', seller.ProductCreateView.as_view(
            extra_context={
                'page_title': 'Ajouter un nouveau produit',
                'page_description': "Ajouter un nouveau produit"
            },
        ), name='product_create'),

        path('update/product/<slug>/',
            seller.ProductUpdateView.as_view(),
            name='product_update'
        ),

        path('delete/product/<slug>/',
            seller.ProductDeleteView.as_view(),
            name='product_delete'
        ),

        path('settings/<slug>/', seller.SettingsUpdateView.as_view(
            extra_context={'page_description': "Configuration"}
        ), name='update'),
    
    ], 'accounts'), namespace='seller')),
]