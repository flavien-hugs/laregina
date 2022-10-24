# category.urls.py

from django.urls import path
from category import views

app_name = 'category'
urlpatterns = [
    path(route='<slug>/', view=views.category_detail_view, name='category_detail'),
]
