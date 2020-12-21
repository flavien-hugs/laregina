# core/urls.py

"""
The `urlpatterns` list routes URLs to views. For more information
    please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('admin/', admin.site.urls),
]
