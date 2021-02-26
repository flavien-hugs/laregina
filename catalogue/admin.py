# catalogue.admin.py

import admin_thumbnails
from django.contrib import admin

from category.models import Category
from catalogue.forms import ProductAdminForm
from catalogue.models import Product, ProductImage

from services.export_data_csv import export_to_csv


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display_links = (
        'name',
        'get_product_shop',
    )
    form = ProductAdminForm
    list_display = [
        'get_product_shop',
        'name',
        'price',
        'get_product_image',
        'is_active'
    ]
    list_filter = [
        'user__store',
        'created_at',
        'is_active',
    ]
    list_editable = (
        "is_active",
    )

    readonly_fields = [
        'get_product_shop',
    ]

    list_per_page = 5
    inlines = [ProductImageInline]
    ordering = ('-created_at',)
    prepopulated_fields = {
        'slug': ('name', 'user',),
        'keywords': ('name',)
    }
    search_fields = ['category', 'name', 'keywords']
    exclude = ('updated_at', 'created_at', 'timestamp')
    actions = [export_to_csv]
