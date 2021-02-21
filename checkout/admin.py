# checkout.admin.py

from django.contrib import admin

from checkout.models import Order, OrderItem
from services.export_data_csv import export_to_csv


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    list_display = [
        'store',
        'name',
        ('quantity', 'total'),
    ]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'

    list_display = [
        'store',
        '__str__',
        'total',
        'date',
        'status',
    ]

    list_filter = [
        'status',
        'date',
    ]

    search_fields = [
        'email',
        'full_name',
        'transaction_id',
        'ip_address',
        'shipping_country',
        'shipping_city',
        'phone',
        'phone_two',
    ]

    fieldsets = (
        ('Information sur la commande',
            {
                'fields': (
                    'email',
                    'status'
                )
            }
        ),
        ('Information sur la livraison',
            {
                'fields': (
                    'user',
                    ('shipping_country', 'shipping_city'),
                    ('shipping_adress', 'shipping_zip'),
                    ('phone', 'phone_two'),
                    'note',
                    'emailing'
                )
            }
        )
    )

    inlines = [OrderItemInline,]
    actions = [export_to_csv]
    search_fields = ['created_at', 'transaction_id']
