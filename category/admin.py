# category.admin.py

from django.contrib import admin

from category.models import Category
from catalogue.models import Product

from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "parent"
    expand_tree_by_default = True
    fieldsets = (
        ('catégorie', {'fields':
            (
                "parent", "name",
                "image", "is_active",
                "slug"
            )}
        ),
    )
    list_per_page = 10
    list_display = (
        "id",
        "tree_actions",
        'indented_title',
        "products_count",
        "is_active",
    )
    mptt_level_indent = 20
    list_display_links = ('indented_title',)
    prepopulated_fields = {"slug": ("parent", "name",)}
