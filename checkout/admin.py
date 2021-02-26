# checkout.admin.py

from django.contrib import admin

from checkout.models import Order, OrderItem
from services.export_data_csv import export_to_csv



class OrderItemStackedInline(admin.StackedInline):
    model = OrderItem
    list_display = [
        'get_store_product',
        'get_product_name',
        ('get_product_price', 'quantity',),
        'total',
    ]
    readonly_fields = [
        'get_store_product',
        'get_product_name',
        'get_product_price',
        'quantity',
        'total'
    ]
    exclude = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    fk_name = "product"
    readonly_fields = [
        'email',
        'shipping_country',
        'shipping_city',
        'shipping_adress',
        'phone', 'phone_two',
        'note', 'shipping_zip',
        'emailing'
    ]
    list_display = [
        'get_order_id',
        'get_shipping_delivery',
        'total', 'date',
        'status',
    ]
    list_editable = (
        "status",
    )
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
        ('Status de la commande',
            {
                'fields': (
                    'status',
                )
            }
        ),
        ('Information sur la livraison',
            {
                'fields': (
                    ('shipping_country', 'shipping_city'),
                    ('shipping_adress', 'shipping_zip'),
                    ('phone', 'phone_two'),
                    'note', 'emailing'
                )
            }
        )
    )
    list_per_page = 5
    inlines = [OrderItemStackedInline,]
    actions = [export_to_csv]
    search_fields = ['created_at', 'transaction_id']
