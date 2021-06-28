# pages.admin.py

from django.contrib import admin

from services.export_data_csv import export_to_csv
from pages.models import Promotion, Contact, Testimonial

@admin.register(Contact)
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


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = [
        'title',
        'category',
        'show_image_tag',
        'created_at',
    ]
    list_filter = [
        'category',
    ]
    list_per_page = 10
    empty_value_display = '-empty-'
    search_fields = ['category', 'title']
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',),}
    actions = [export_to_csv]


@admin.register(Testimonial)
class PromotionAdmin(admin.ModelAdmin):
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
