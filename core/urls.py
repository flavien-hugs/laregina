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
from pages.views import subscribeView
from accounts.views import customer, seller


admin.autodiscover()

def handler404(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=404,
        context={'page_title': 'Page non trouvée - {{ status }}'})

def handler403(request, exception, template_name='403.html'):
    return render(request, template_name=template_name, status=403,
        context={'page_title': 'Page non trouvée - {{ status }}'})

def handler500(request, template_name='500.html'):
    return render(request, template_name=template_name,
        status=500, context={'page_title': '{{ status }}'})


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('x-admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name="search"),
    path('c/', include('category.urls', namespace='category')),
    path('p/', include('catalogue.urls', namespace='catalogue')),
    path('avis/', include('reviews.urls', namespace='reviews')),
    path('panier/', include('cart.urls', namespace='cart')),
    path('checkout/', include('order.urls', namespace='order')),
    path('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    path('abonnement/', subscribeView, name='subscribe'),
    path('sp-', include("pages.urls", namespace='pages')),
    path('pgs/', include("core.pages.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', include('accounts.urls')),
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
