# pages.admin.py

from django.contrib import admin

from services.export_data_csv import export_to_csv

from pages import models, forms

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = [
        'full_name',
        'company',
        'email',
        'phone',
        'subject',
    ]

    list_filter = [
        'timestamp',
        'subject',
        'company'
    ]

    list_per_page = 50
    empty_value_display = '-empty-'
    search_fields = ['subject', 'email', 'company']
    list_display_links = ('email', 'full_name')
    readonly_fields = (
        'timestamp',
        'full_name',
        'company',
        'phone',
        'email',
        'subject',
        'message',
    )
    actions = [export_to_csv]


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    form = forms.PromotionForm
    date_hierarchy = 'created_at'
    fieldsets = (
        (
            'produit en promotions', {
            'classes': ('collapse',),
            'fields':
                (   
                    "product",
                    ("name", "slug"),
                )
            }
        ),
        (
            'cover de la promotion', {
            'classes': ('collapse',),
            'fields':
                (
                    "image", "active",
                )
            }
        ),
    )
    list_display = [
        'get_store',
        'name',
        'show_image_tag',
        'created_at',
    ]
    list_filter = [
        'product',
        'active'
    ]
    list_per_page = 10
    search_fields = ['name']
    actions = [export_to_csv]
    list_display_links = ('name',)
    empty_value_display = '-empty-'
    prepopulated_fields = {'slug': ('name',),}


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = [
        'full_name',
        'status_client',
        'created_at',
    ]
    list_per_page = 10
    empty_value_display = '-empty-'
    list_display_links = ('full_name',)
    actions = [export_to_csv]