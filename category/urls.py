# category.urls.py

from django.urls import path
from category.views import CategoryListView, CategoryDetailView

app_name = 'category'
urlpatterns = [
    path('list/', CategoryListView.as_view(), name='category_list'),
    path('<slug>/', CategoryDetailView.as_view(), name='category_detail'),
]
