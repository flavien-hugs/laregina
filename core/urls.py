# core/urls.py

"""
The `urlpatterns` list routes URLs to views. For more information
    please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('dashboard/', include("core.pages.urls")),

    # Remove logout confirmation
    # Note: Needs to be changed to redirect to ACCOUNT_LOGOUT_REDIRECT_URL
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    path('accounts/', include('allauth.urls')),
    path('vendor/', include('accounts.urls', namespace='accounts')),
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
