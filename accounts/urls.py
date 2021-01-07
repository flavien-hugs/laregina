# accounts/urls.py

from django.urls import path
from accounts.views import StoreProfileSelfDetailView, StoreProfileDetailView, StoreProfileUpdateView

app_name = 'accounts'
urlpatterns = [
    path('store/', StoreProfileSelfDetailView.as_view(
        extra_context={'page_title': 'Tableau de bord',
        'page_description': "Tableau de bord"}), name='profile'),

    path('store/<slug>/', StoreProfileDetailView.as_view(), name='detail'),

    # Profile is updated in settings
    path('settings/store/', StoreProfileUpdateView.as_view(
        extra_context={'page_title': 'Configuration', 'page_description': "Configuration"
        }), name='update'),
]