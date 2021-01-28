# cart.admin.py

from django.contrib import admin

from cart.models import CartItem
from cart.services.cart_csv import export_to_csv


admin.site.register(CartItem)
# admin.site.register(Cart)

# class ItemCartAdmin(admin.TabularInline):
#     date_hierarchy = 'timestamp'
#     model = CartItem

#     list_display = [
#         'get_product_name',
#         'get_shop_name',
#         'get_product_price',
#         'quantity',
#         'updated'
#     ]

#     ordering = [
#         'timestamp',
#         'updated'
#     ]

#     list_filter = [
#         'user__store',
#         'updated',
#         'timestamp',
#     ]

#     list_display_links = ('get_product_name', 'get_shop_name')
#     search_fields = ['get_shop_name', 'get_product_name']


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     date_hierarchy = 'timestamp'
#     list_display = [
#         'get_shop_name',
#         'user',
#         'total',
#         'timestamp',
#         'active'
#     ]

#     ordering = [
#         'total',
#         'timestamp',
#         'updated'
#     ]

#     list_filter = [
#         'updated',
#         'timestamp',
#     ]

#     list_per_page = 50
#     inlines = [ItemCartAdmin]
#     search_fields = ['total', 'get_shop_name']
#     list_display_links = ('user', 'get_shop_name')
#     actions = [export_to_csv]
