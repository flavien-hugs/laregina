# analytics.admin.py

from django.contrib import admin

from analytics.models import ProductView 


@admin.register(ProductView)
class AnalyticsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_viewed'

    list_display = [
        'user',
        'ip_address',
        'product',
        'date_viewed',
        'time_viewed'
    ]

    readonly_fields = [
        'tracking_id',
        'ip_address',
        'product',
        'date_viewed',
        'time_viewed'
    ]

    list_filter = [
        'product',
        'ip_address',
        'date_viewed',
        'time_viewed'
    ]
