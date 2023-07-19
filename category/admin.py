from catalogue.models import Product
from category.models import Category
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    max_num = 1
    verbose_name = "produits"
    show_change_link = True
    raw_id_fields = ["user"]
    list_display = ["name", "price"]
    exclude = [
        "updated_at",
        "created_at",
        "description",
        "keywords",
        "is_external",
        "slug",
        "quantity",
    ]


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    mptt_indent_field = "parent"
    expand_tree_by_default = False
    fieldsets = (
        ("catégorie", {"fields": ("parent", "name", "image", "is_active", "slug")}),
    )
    mptt_level_indent = 20
    prepopulated_fields = {
        "slug": (
            "parent",
            "name",
        )
    }
    inlines = [ProductInline]
    actions = ["make_disabled"]

    @admin.action(description="Mark selected categories as disabled")
    def make_disabled(self, request, queryset):
        queryset.update(is_active=False)
