# pages.admin.py

from django.contrib import admin
from django.utils.safestring import mark_safe

from pages.models import Promotion, Subscribe, Contact
from services.export_data_csv import export_to_csv


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = [
        'email',
        'timestamp',
    ]
    ordering = [
        'timestamp',
    ]
    list_filter = [
        'timestamp',
    ]

    list_display_links = ('email',)
    search_fields = ['email',]


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
    fields = (
        'category',
        'title',
        'image',
        'link_to'
    )
    list_per_page = 50
    empty_value_display = '-empty-'
    search_fields = ['category', 'title']
    list_display_links = ('title',)
    prepopulated_fields = {'link_to': ('title',),}
    actions = [export_to_csv]

    def show_image_tag(self, obj):
        if obj.image is not None:
            return mark_safe('<img src="{url}" height="50"/>'.format(url=obj.image.url))
        else:
            return ""
