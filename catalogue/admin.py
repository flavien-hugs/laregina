# catalogue.admin.py

import admin_thumbnails
from django.contrib import admin

from category.models import Category
from catalogue.forms import ProductAdminForm
from catalogue.models import Product, Variation, ProductImage


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 3


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    date_hierarchy = 'created_at'
    list_display_links = ('name',)

    list_display = [
        'name',
        'price',
        'recomended_product',
        'show_image_tag',
        'is_stock',
        'is_active'
    ]

    list_filter = [
        'is_stock',
        'is_active',
        'created_at',
        'nb_view',
    ]

    list_editable = (
        "is_active",
        "is_stock",
        "is_active",
    )

    list_per_page = 50
    inlines = [VariationInline, ProductImageInline]
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['category', 'name', 'keywords']
    exclude = ('updated_at', 'created_at', 'timestamp')

    class Meta:
        model = Product
