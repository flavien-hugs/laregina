# core/urls.py

"""
The `urlpatterns` list routes URLs to views. For more information
    please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from analytics import utils
from search.views import SearchView
from accounts.views import customer, seller
from checkout.views import TrackOrderView, download_invoice_view


admin.autodiscover()


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=404,
        context={'page_title': 'Page non trouvée'})

def handler403(request, exception, template_name='403.html'):
    return render(request, template_name=template_name, status=403,
        context={'page_title': 'Page non trouvée'})

def handler500(request, template_name='500.html'):
    return render(request, template_name=template_name,
        status=500, context={'page_title': 'Erreur interne'})


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('lrg-admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name="search"),
    path('c/', include('category.urls', namespace='category')),
    path('p/', include('catalogue.urls', namespace='catalogue')),
    path('avis/', include('reviews.urls', namespace='reviews')),
    path('panier/', include('cart.urls', namespace='cart')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('tracking/order/', TrackOrderView.as_view(extra_context={
        'page_title': 'Suivi votre commande',}), name='order_tracking'),
    path('print-invoice/<int:order_id>/', download_invoice_view, name='download_invoice'),
    path('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    path('sp-', include("pages.urls", namespace='pages')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path('magasin/<slug>/', seller.StoreDetailView.as_view(), name='store_detail_view'),
]

handler404 = handler404
handler403 = handler403
handler201600 = handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('404', handler404, {'exception': Exception()}),
        path('403', handler403, {'exception': Exception()}),
        path('500', handler500),
    ]
