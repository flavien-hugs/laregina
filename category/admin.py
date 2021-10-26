# category.admin.py

from django.contrib import admin
from django.utils.html import format_html

from category.models import Category
from catalogue.models import Product

from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    mptt_indent_field = "parent"
    expand_tree_by_default = False

    fieldsets = (
        ('catégorie', {'fields':
            (   
                "parent", 
                ("name", "slug"),
                "image",
                "is_active",
            )}
        ),
    )
    list_per_page = mptt_level_indent
    list_display = (
        'id', 'tree_actions', 'indented_title',
        'related_products_cumulative_count'
    )
    list_display_links = ('id', 'indented_title',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_cumulative_count', cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, 'category', 'products_count', cumulative=True)
        return qs

    @admin.display(description="nombre de produits similaires")
    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
