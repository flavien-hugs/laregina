# pages.admin.py

from django.contrib import admin

from pages.models import Subscribe, Contact
from cart.services.cart_csv import export_to_csv


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

    ordering = [
        'timestamp',
        'subject'
    ]

    list_filter = [
        'timestamp',
        'subject',
        'company'
    ]

    list_per_page = 50
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
