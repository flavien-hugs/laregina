# order.admin.py

from django.contrib import admin

from order.models import Order, Address


class AddressAdmin(admin.TabularInline):
    model = Address
    readonly_fields = ('id',)
    max_num = 4
    list_display = ['country', 'region', 'city', 'street', 'zip_code', 'phone_1', 'phone_2']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = [
        'track_order',
        'timestamp',
        'create_date'
    ]
    search_fields = ['create_date', 'track_order']
