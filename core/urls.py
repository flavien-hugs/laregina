from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.urls import path, include
from django.contrib.sitemaps import views
from django.conf.urls.static import static
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.views.generic import TemplateView

from core.sitemap import SITEMAPS
from search.views import search_view

from django_summernote.models import Attachment




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
    path(settings.ADMIN_URL, admin.site.urls),
    path('sp-', include("pages.urls", namespace='pages')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('', include('catalogue.urls')),
    path(route='catalog/', view=search_view, name="search"),

    path('jet/', include('jet.urls', 'jet')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('accounts.urls')),

    # path(route='', view=catalog_views.home_view, name='home'),
    # path(route='mon-marche/', view=catalog_views.market_view, name='market'),
    # path(route='monmarche/', view=catalog_views.home_market_view, name='homemarket'),

    path('sitemap.xml', views.sitemap,
        {'sitemaps': SITEMAPS},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler403 = handler403
handler201600 = handler500

admin.site.site_header = "LAREGINA DEALS ADMIN"
admin.site.site_title = "LAREGINA DEALS ADMIN"

if settings.DEBUG:
    urlpatterns += [
        path('404', handler404, {'exception': Exception()}),
        path('403', handler403, {'exception': Exception()}),
        path('500', handler500),
    ]
