# order.admin.py

from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'

    list_display = [
        'user',
        'transaction_id',
        '__str__',
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
