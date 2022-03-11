# category.admin.py

from django.contrib import admin

from category.models import Category
from catalogue.models import Product

from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    model = Category
    list_per_page = 10
    mptt_level_indent = 10
    mptt_indent_field = "parent"
    expand_tree_by_default = False
    
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('catégorie', {'fields':
            (   
                "parent", "name",
                "image", "is_active",
            )}
        ),
    )
    list_per_page = 10
    list_display = (
        "id",
        'tree_actions',
        'indented_title',
        "products_count",
        "is_active",
    )
    list_display_links = ('id', 'indented_title',)