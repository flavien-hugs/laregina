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
    extra = 1
    max_num = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display_links = ('name',)
    form = ProductAdminForm
    list_display = [
        'name',
        'price',
        'show_image_tag',
        'is_active'
    ]

    list_filter = [
        'is_active',
        'created_at',
    ]

    list_editable = (
        "is_active",
    )

    list_per_page = 5
    inlines = [ProductImageInline]
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',), 'keywords': ('name',)}
    search_fields = ['category', 'name', 'keywords']
    exclude = ('updated_at', 'created_at', 'timestamp')
    actions = [export_to_csv]
