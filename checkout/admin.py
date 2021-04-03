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
        'get_order_payment',
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
    actions = [
        export_to_csv,
        'make_submitted',
        'make_shipped',
        'make_cancelled',
        'make_processed'
    ]
    search_fields = ['created_at', 'transaction_id']


    def make_submitted(self, request, queryset):
        queryset.update(status='SUBMITTED')
    make_submitted.short_description = 'Marquer comme en cours de traitement'

    def make_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
    make_shipped.short_description = 'Marquer comme livrée'

    def make_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
    make_cancelled.short_description = 'Marquer comme annulée'

    def make_processed(self, request, queryset):
        queryset.update(status='PROCESSED')
    make_processed.short_description = 'Marquer comme en cours de livraison'
