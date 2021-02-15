# cart.admin.py

from django.contrib import admin

from cart.models import CartItem
from services.export_data_csv import export_to_csv


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = [
        'cart_id',
        'get_shop_name',
        'name',
        'quantity',
        'price',
        'total',
    ]
    list_per_page = 50
    list_filter = ('created_at',)
    search_fields = ['total', 'get_shop_name']
    list_display_links = ('cart_id', 'get_shop_name')
    actions = [export_to_csv]
