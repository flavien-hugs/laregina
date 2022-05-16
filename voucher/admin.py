# voucher.admin.py

from django.contrib import admin

from voucher.models import Voucher
from catalogue.models import Product


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    model = Voucher
    date_hierarchy = 'created_at'
    fieldsets = (
        (
            'Information la réduction', {
                "fields": (
                    "user", "discount",
                    "is_active",
                )
            },
        ),
        (
            'Produits', {
                "fields": (
                    "products",
                )
            },
        ),
    )
    list_display = (
        "user",
        "get_discount",
        "get_products_count",
        "is_active",
    )
    list_display_links = (
        "user",
    )
    list_editable = (
        "is_active",
    )
    list_filter = (
        "user",
        'is_active',
    )
    list_per_page = 15
