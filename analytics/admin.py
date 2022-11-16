# analytics.admin.py

from django.contrib import admin

from analytics.models import ProductView
from services.export_data_csv import export_to_csv


# @admin.register(ProductView)
class AnalyticsAdmin(admin.ModelAdmin):
    date_hierarchy = "date_viewed"

    list_display = ["ip_address", "product", "date_viewed", "time_viewed"]

    readonly_fields = ["ip_address", "product", "date_viewed", "time_viewed"]

    list_filter = ["product", "ip_address", "date_viewed", "time_viewed"]
    actions = [export_to_csv]
