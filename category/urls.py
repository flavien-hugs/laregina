# category.urls.py

from django.urls import path
from category.views import category_detail_view

app_name = 'category'
urlpatterns = [
    path(route='<slug>/', view=category_detail_view, name='category_detail'),
]
