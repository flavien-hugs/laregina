# order.admin.py

from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    list_display = [
        'store',
        'name',
        'quantity',
        'total',
    ]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'

    list_display = [
        '__str__',
        'transaction_id',
        'user',
        'date',
        'status',
        'emailing'
    ]

    list_filter = ('status', 'date', 'emailing')

    search_fields = [
        'email',
        'full_name',
        'transaction_id',
        'ip_address',
        'emailing'
    ]

    fieldsets = (
        ('Information de commande',
            {
                'fields': (
                    'status',
                    'email',
                    'phone',
                )
            }
        ),
        ('Information de livraison',
            {
                'fields': (
                    'user',
                    'shipping_address',
                    'shipping_city',
                    'shipping_zip',
                    'shipping_country'
                )
            }
        )
    )

    inlines = [OrderItemInline,]
    search_fields = ['created_at', 'transaction_id']
