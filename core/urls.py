from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.urls import path, include
from django.contrib.sitemaps import views
from django.conf.urls.static import static
from django.views.generic import TemplateView

from search.views import search_view
from checkout.views import track_order_view, download_invoice_view

from core.sitemap import SITEMAPS
from catalogue import views as catalog_views

from allauth.account.models import EmailAddress
from django_summernote.models import Attachment

admin.site.unregister(Attachment)
admin.site.unregister(EmailAddress)


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
    path(route='', view=catalog_views.combine_view, name='home'),
    path(route='search/', view=search_view, name="search"),
    path('', include('catalogue.urls')),
    path('categorie/', include('category.urls', namespace='category')),
    path('avis/', include('reviews.urls', namespace='reviews')),
    path('panier/', include('cart.urls', namespace='cart')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path(route='tracking/order/', view=track_order_view, name='order_tracking'),
    path(route='print-invoice/<int:order_id>/',
        view=download_invoice_view, name='download_invoice'),
    path('sp-', include("pages.urls", namespace='pages')),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),

    path('jet/', include('jet.urls', 'jet')),
    path('summernote/', include('django_summernote.urls')),
    path(settings.ADMIN_URL, admin.site.urls),

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
