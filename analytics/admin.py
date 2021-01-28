# analytics.admin.py

from django.contrib import admin

from analytics.models import ProductView 


@admin.register(ProductView)
class AnalyticsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_viewed_at'

    list_display = [
        'user',
        'ip_address',
        'product',
        'date_viewed_at',
        'time_viewed_at'
    ]

    readonly_fields = [
        'tracking_id',
        'ip_address',
        'product',
        'date_viewed_at',
        'time_viewed_at'
    ]

    list_filter = [
        'product',
        'ip_address',
        'date_viewed_at',
        'time_viewed_at'
    ]
