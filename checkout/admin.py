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
    model = Order
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
        'get_order_payment',
        'get_order_rest_payment',
        'get_order_total',
        'date', 'status',
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
    ]

    fieldsets = (
        ('Status de la commande',
            {
                'fields': (
                    ('status', 'email'),
                )
            }
        ),
        ('Information sur la commande',
            {
                'fields': (
                    ('shipping_country', 'shipping_city'),
                    ('shipping_adress', 'shipping_zip'),
                    ('phone', 'phone_two'),
                    'note', 'emailing',
                )
            }
        )
    )
    list_per_page = 10
    inlines = [OrderItemStackedInline,]
    actions = [
        export_to_csv,
        'make_submitted',
        'make_shipped',
        'make_cancelled',
        'make_processed'
    ]
    search_fields = ['created_at', 'transaction_id']

    @admin.display(description="commande en cours de traitement")
    def make_submitted(self, request, queryset):
        queryset.update(status='SUBMITTED')

    @admin.display(description="commande livrée")
    def make_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')

    @admin.display(description="commande annulée")
    def make_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')

    @admin.display(description="commande en cours de livraison")
    def make_processed(self, request, queryset):
        queryset.update(status='PROCESSED')
