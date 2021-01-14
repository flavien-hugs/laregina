# catalogue.admin.py

import admin_thumbnails
from django.contrib import admin

from category.models import Category
from catalogue.models import Product, ProductImage


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('id',)
    extra = 1
    max_num = 4


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'name', 'image_thumbnail']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display_links = ('__str__',)

    list_display = [
        '__str__',
        'current_price',
        'show_image_tag',
        'is_stock',
        'is_active'
    ]

    list_filter = [
        'price',
        'old_price',
        'is_stock',
        'is_active',
        'created_at'
    ]

    list_editable = (
        "is_active",
        "is_stock",
        "is_active",
    )

    list_per_page = 50
    readonly_fields = ('show_image_tag', 'quantity')
    inlines = [ProductImageInline]
    ordering = ('created_at',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['category', 'name']

    class Meta:
        model = Product
        
    def current_price(self, obj):
        if obj.old_price > 0:
            return obj.old_price
        else:
            return obj.price
