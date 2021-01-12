# cart.admin.py

from django.contrib import admin

from cart.models import Cart, CartItem
from cart.services.cart_csv import export_to_csv


class ItemCartAdmin(admin.TabularInline):
    model = CartItem
    readonly_fields = ('id',)
    max_num = 4
    list_display = ['product__user', 'product__name', 'quantity', 'timestamp']


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = [
        'user',
        'total',
        'timestamp',
        'active'
    ]
    inlines = [ItemCartAdmin]
    ordering = [
        'total',
        'timestamp',
        'updated'
    ]
    search_fields = ['total', 'user']
    actions = [export_to_csv]
