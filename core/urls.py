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

from accounts.views import customer, seller
from category.views import CategoryListView, CategoryDetailView

admin.autodiscover()

def handler404(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=404,
        context={'page_title': 'Page non trouvée - Erreur 404'})

def handler403(request, exception, template_name='403.html'):
    return render(request, template_name=template_name, status=403,
        context={'page_title': 'Page non trouvée - Erreur 404'})

def handler500(request, template_name='500.html'):
    return render(request, template_name=template_name,
        status=500, context={'page_title': 'Erreur interne'})

def home(request, template='index.html'):
    # if request.user.is_authenticated:
    #     if request.user.is_seller:
    #         return redirect('accounts:profile')
    #     elif request.user.is_buyer:
    #         return redirect('customer:customer_dashboard')
    return render(request, template)


urlpatterns = [
    path('', home, name='home'),
    path('', include('category.urls', namespace='category')),
    path('', include("core.pages.urls")),
    path('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

handler404 = handler404
handler403 = handler403
handler201600 = handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('404', handler404, {'exception': Exception()}),
        path('403', handler403, {'exception': Exception()}),
        path('500', handler500),
    ]
