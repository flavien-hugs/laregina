# category.admin.py

from django.contrib import admin

from category.models import Category
from catalogue.models import Product

from mptt.admin import DraggableMPTTAdmin


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    max_num = 1
    verbose_name = "produits"
    show_change_link = True
    raw_id_fields = ['user']
    list_display = ['name', 'price']
    exclude = [
        'updated_at', 'created_at',
        'description', 'keywords', 'is_external',
        'slug', 'quantity'
    ]


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "parent"
    expand_tree_by_default = False
    fieldsets = (
        ('catégorie', {'fields':
            (
                "parent", "name",
                "image", "is_active",
                "slug"
            )}
        ),
    )
    list_display = (
        "id",
        "tree_actions",
        'indented_title',
        "products_count",
        "is_active",
    )
    mptt_level_indent = 20
    list_filter = ("parent__name",)
    list_display_links = ('indented_title',)
    prepopulated_fields = {"slug": ("parent", "name",)}
    inlines = [ProductInline]
