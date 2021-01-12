# category.admin.py

from django.contrib import admin
from django.utils.html import format_html

from category.models import Category
from catalogue.models import Product

from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 20

    list_display = (
        'tree_actions', 'indented_title',
        'related_products_count',
        'related_products_cumulative_count'
    )

    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (('parent', TreeRelatedFieldListFilter),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_cumulative_count', cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_count', cumulative=True)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Produits similaires (pour cette catégorie spécifique)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Produits similaires'
