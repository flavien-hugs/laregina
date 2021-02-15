# category.urls.py

from django.urls import path
from category.views import CategoryDetailView

app_name = 'category'
urlpatterns = [
    path('<slug>/', CategoryDetailView.as_view(), name='category_detail'),
]
