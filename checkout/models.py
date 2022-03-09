# checkout.models.py

import decimal
import random
import string
import datetime

from django.db import models
from django.urls import reverse
from django.contrib import admin

from core import settings
from catalogue.models import Product
from checkout.managers import OrderManager
from helpers.models import BaseOrderInfo, BaseTimeStampModel

NULL_AND_BLANK = {'null': True, 'blank': True}


class Order(BaseOrderInfo, BaseTimeStampModel):

    SHIPPED = 'livrée'
    CANCELLED = 'annulée'
    PROCESSED = 'livraison en cours'
    SUBMITTED = 'traitement en cours'

    ORDER_STATUS = (
        (SUBMITTED, 'traitement en cours'),
        (PROCESSED, 'livraison en cours'),
        (SHIPPED, 'livrée'),
        (CANCELLED, 'annulée'),
    )

    status = models.CharField(
        verbose_name='status',
        max_length=120,
        choices=ORDER_STATUS,
        default=SUBMITTED
    )
    transaction_id = models.CharField(
        verbose_name='id de la commande',
        unique=True,
        max_length=20,
        **NULL_AND_BLANK
    )
    ip_address = models.CharField(
        verbose_name='adresse ip',
        max_length=50,
        **NULL_AND_BLANK
    )
    emailing = models.BooleanField(
        verbose_name='abonnement aux offres et promotions',
        default=False
    )
    date = models.DateTimeField(
        verbose_name='date de la commade',
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        verbose_name='derniere modification',
        auto_now=True
    )

    objects = OrderManager()

    class Meta:
        verbose_name_plural = 'commandes'

    def __str__(self):
        return f'#{self.transaction_id} - {self.status}'

    @admin.display(description="n° commande")
    def get_order_id(self):
        return self.transaction_id

    @admin.display(description="nom")
    def get_short_name(self):
        return f'{self.shipping_first_name}'

    @admin.display(description="nom & prénoms")
    def get_full_name(self):
        return f'{self.get_short_name()} {self.shipping_last_name}'

    @admin.display(description="adresse de livraison")
    def get_shipping_delivery(self):
        return f'{self.shipping_country.name}, {self.shipping_city}, {self.shipping_adress} | {self.phone}'

    def get_shipping_delivery_for_seller(self):
        return f'{self.shipping_city}, {self.shipping_country.name}'

    def save(self, *args, **kwargs):
        if self.transaction_id is None:
            self.generate(8)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.transaction_id = 'LC-{}'.format(today + ''.join(random_carac))

    def order_items(self):
        order_items = OrderItem.objects.filter(order=self)
        return order_items

    @admin.display(description="montant commande")
    def get_order_total(self):
        total = decimal.Decimal('0')
        for item in self.order_items():
            total += item.total
        total = total + 1500
        return total

    @admin.display(description="montant réglé")
    def get_order_payment(self):
        order_total = self.get_order_total()
        payment_advance = int('0')
        min_amount = int('10000')
        percent_amount = decimal.Decimal('0.5')
        if order_total >= min_amount:
            payment_advance = order_total * percent_amount
        elif order_total <= min_amount:
            payment_advance = order_total
        return payment_advance

    @admin.display(description="reste à payé")
    def get_order_rest_payment(self):
        payment_rest = int("0")
        order_total = self.get_order_total()
        order_advance = self.get_order_payment()
        payment_rest = float(order_total - order_advance)
        return payment_rest

    @admin.display(description="cash du vendeur")
    def total_seller_order(self):
        total_se_ = self.get_order_total() - 1500
        return total_se_

    @admin.display(description="commission")
    def get_cost(self):
        percent = decimal.Decimal('0.05')
        cost = self.total_seller_order() * percent
        return cost

    @admin.display(description="coût total")
    def total_order(self):
        total_or_ = self.total_seller_order() - self.get_cost()
        return total_or_

    @admin.display(description="cash total")
    def get_total_sales(self):
        total = decimal.Decimal(0)
        orders = self.order_items()
        for item in orders:
            total += item.total_order()
        return total

    def get_absolute_url(self):
        return reverse('seller:order_detail', kwargs={'pk': int(self.id)})

    def get_success_url(self):
        return reverse('checkout:order_success', kwargs={'pk': int(self.transaction_id)})


class OrderItem(models.Model):

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name='commande'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name='produit'
    )
    quantity = models.IntegerField(
        verbose_name='quantité',
        default=1
    )
    date_updated = models.DateTimeField(
        verbose_name='derniere modification',
        auto_now=True,
        auto_now_add=False
    )
    date_created = models.DateTimeField(
        verbose_name='date ajout',
        auto_now=True,
        auto_now_add=False
    )

    class Meta:
        db_table = 'checkout_order_item_db'
        ordering = ['-date_created', '-date_updated']
        get_latest_by = ['-date_created', '-date_updated']
        verbose_name_plural = 'panier'

    def __str__(self):
        return self.product.name

    @property
    def total(self):
        return self.quantity * self.product.price

    @admin.display(description="prix unitaire")
    def get_product_price(self):
        return self.product.price

    @admin.display(description="produit")
    def get_product_name(self):
        return self.product.name

    @admin.display(description="N° de téléphone")
    def get_phone_number(self):
        return self.product.user.phone

    @admin.display(description="contact boutique")
    def get_store_product(self):
        return f'{self.product.user.store} | {self.get_phone_number()}'

    @admin.display(description="boutique")
    def get_store_name(self):
        return self.product.user.store

    def get_absolute_url(self):
        return self.product.get_absolute_url()


from django.dispatch import receiver
@receiver(models.signals.pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_order_id_generator(instance)
