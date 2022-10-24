from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from catalogue import models, forms
from services.export_data_csv import export_to_csv
from django_summernote.admin import SummernoteModelAdmin


class ProductImageInline(admin.TabularInline):
    extra = 0
    max_num = 3
    show_change_link = True
    model = models.ProductImage
    readonly_fields = ['product']


class ProductAttributeValueAdmin(admin.TabularInline):
    model = models.ProductAttributeValue
    extra = 2



@admin.register(models.Product)
class ProductAdmin(SummernoteModelAdmin):
    model = models.Product
    date_hierarchy = 'created_at'
    fieldsets = (
        ('information sur le produit', {'fields':
            (
                "user",
                "category",
                ("name", "price"),
            )}
        ),
        (
            'description du produit',
            {
                'classes': ('collapse',),
                'fields': [
                    'description', 'keywords',
                    ("is_external", "is_active"),
                ],
            }
        ),
    )
    list_display_links = (
        'name',
        'get_product_shop',
    )
    list_display = [
        'get_product_shop', 'category', 'name',
        'price', 'get_vouchers', 'get_vouchers_price',
        'product_link', 'is_active', 'get_product_image',
    ]
    list_filter = [
        'user__store',
        'category'
    ]
    list_editable = (
        'category',
        "is_active",
    )
    readonly_fields = [
        'get_product_shop',
    ]
    list_per_page = 10
    inlines = [ProductAttributeValueAdmin, ProductImageInline]
    prepopulated_fields = {
        'keywords': ('name',)
    }
    search_fields = ['category', 'name', 'keywords']
    exclude = ('updated_at', 'created_at', 'timestamp')
    actions = [export_to_csv]

    @mark_safe
    @admin.display(description="Voir le produit")
    def product_link(self, instance):
        if instance.slug:
            product_url = instance.get_absolute_url()
            link = f"""
                <a title="view {instance.name} on website"
                    target="_blank" href="{product_url}">
                    Voir
                </a>
            """
            return format_html(link)
        else:
            return 'Aucun lien'
