# static pages url

from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from pages.views import ContactView

app_name = 'pages'
urlpatterns  = [
    path('contact/', ContactView.as_view(), name='contact'),

    path('about-us/',
        cache_page(CACHE_TTL)(TemplateView.as_view(
            extra_context={
            'page_title': 'À propos de nous',
            'page_description': "Qui sommes-nous ?"
        }, template_name='pages/about-us.html')), name='about-us'),
    
    path('faq/',
        cache_page(CACHE_TTL)(TemplateView.as_view(
            extra_context={
            'page_title': 'FAQs : Questions fréquemment posées',
            'page_description': "Questions fréquemment posées"
        }, template_name='pages/faqs.html')), name='faqs'),
    
    path('condition-generale-utilisation/',
        cache_page(CACHE_TTL)(TemplateView.as_view(
            extra_context={
            'page_title': "Conditions Générales d'Utilisation",
            'page_description': "Conditions Générales d'Utilisation"
        }, template_name='pages/cgu.html')), name='cgu'),
    
    path('politique-confidentialite/',
        cache_page(CACHE_TTL)(TemplateView.as_view(
            extra_context={
            'page_title': "Politique de Confidentialité",
            'page_description': "Politique de Confidentialité"
        }, template_name='pages/terms.html')), name='terms'),
]
