# accounts/urls.py

from django.urls import path
from accounts.views import StoreProfileSelfDetailView, StoreProfileDetailView, StoreProfileUpdateView


app_name = 'accounts'
urlpatterns = [
    path('store/', StoreProfileSelfDetailView.as_view(), name='profile'),
    path('store/<slug>/', StoreProfileDetailView.as_view(), name='detail'),

    # Profile is updated in settings
    path('settings/store/', StoreProfileUpdateView.as_view(), name='update'),
]