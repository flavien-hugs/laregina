# checkout.models.py

import decimal
import random
import string
import datetime
from django.db import models
from django.urls import reverse

from core import settings
from catalogue.models import Product
from checkout.managers import OrderManager

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# user manager
User = settings.AUTH_USER_MODEL

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'blank': True, 'max_digits': 50, 'decimal_places': 2}


class BaseOrderInfo(models.Model):

    class Meta:
        abstract = True

    email = models.EmailField(
        verbose_name='adresse de messagerie',
        max_length=50
    )
    shipping_first_name = models.CharField(
        verbose_name='nom de famille',
        max_length=50
    )
    shipping_last_name = models.CharField(
        verbose_name='prénom',
        max_length=50
    )
    phone = PhoneNumberField('numéro de téléphone')

    phone_two = PhoneNumberField(
        verbose_name='téléphone supplémentaire (facultatif)',
        blank=True
    )
    shipping_city = models.CharField(
        verbose_name='ville',
        max_length=50
    )
    shipping_country = CountryField(
        blank_label='sélection un pays',
        verbose_name='pays/région',
        multiple=False
    )
    shipping_adress = models.CharField(
        verbose_name='situation géographique',
        max_length=50
    )
    shipping_zip = models.CharField(
        verbose_name='adresse postal (facultatif)',
        max_length=10,
        **NULL_AND_BLANK
    )
    note = models.TextField(
        verbose_name='note de commande (facultatif)',
        max_length=120,
        **NULL_AND_BLANK
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(BaseOrderInfo):

    SHIPPED = 'Commande livrée'
    CANCELLED = 'Commande annulée'
    PROCESSED = 'Commande en cours de livraison'
    SUBMITTED = 'Commande en cours de traitement'

    ORDER_STATUSES = (
        (SUBMITTED, 'Commande en cours de traitement'),
        (PROCESSED, 'Commande en cours de livraison'),
        (SHIPPED, 'Commande livrée'),
        (CANCELLED, 'Commande annulée'),
    )
    status = models.CharField(
        verbose_name='status',
        max_length=120,
        choices=ORDER_STATUSES,
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
        verbose_name_plural = 'commande'
    
    def __str__(self):
        return '#{transaction_id}'.format(
            transaction_id=self.transaction_id)

    def get_order_id(self):
        return '#{transaction_id}'.format(
            transaction_id=str(self.transaction_id)
        )
    get_order_id.short_description='N° commande'

    def get_short_name(self):
        return '{first_name}'.format(
            first_name=self.shipping_first_name
        )
    get_short_name.short_description='Nom'

    def get_full_name(self):
        return '{short_name} {last_name}'.format(
            short_name=self.get_short_name(),
            last_name=self.shipping_last_name
        )
    get_full_name.short_description='Nom & prénoms'

    def get_shipping_delivery(self):
        return '{shipping_country}, {shipping_city}, {shipping_adress} | {shipping_phone}/{shipping_phone_two}'.format(
            shipping_country=self.shipping_country.name,
            shipping_city=self.shipping_city,
            shipping_adress=self.shipping_adress,
            shipping_phone=self.phone,
            shipping_phone_two=self.phone_two
        )
    get_shipping_delivery.short_description='Adresse de livraison'

    def get_shipping_delivery_for_seller(self):
        return '{shipping_country}, {shipping_city}, {shipping_adress}'.format(
            shipping_country=self.shipping_country.name,
            shipping_city=self.shipping_city,
            shipping_adress=self.shipping_adress,
        )

    def save(self, *args, **kwargs):
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

    @property
    def total(self):
        total = decimal.Decimal('0')
        for item in self.order_items():
            total += item.total
        return total + 1500

    # cash du vendeur
    @property
    def total_seller(self):
        total = decimal.Decimal('0')
        for item in self.order_items():
            total += item.total
        return total

    # cout de la commande pour le vendeur
    # sans les frais
    def total_seller_order(self):
        fee =  1500
        total = self.total_seller - fee
        return total

    # calcul de la commission
    def get_cost(self):
        percent = decimal.Decimal('0.05')
        cost = self.total_seller_order() * percent
        return cost

    # cout total apres commission
    def total_order(self):
        total = self.total_seller_order() - self.get_cost()
        return total

    # cash apres commission
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
    
    """
    classe modèle pour le stockage de chaque instance
    de produit commander dans chaque commande
    """

    order = models.ForeignKey(
        Order,
        models.CASCADE,
        verbose_name='commande'
    )
    product = models.ForeignKey(
        Product,
        models.CASCADE,
        verbose_name='produit'
    )
    quantity = models.IntegerField(
        verbose_name='quantité',
        default=1
    )
    date_updated = models.DateTimeField(
        verbose_name='derniere modification',
        auto_now=True
    )
    date_created = models.DateTimeField(
        verbose_name='date ajout',
        auto_now=True
    )

    class Meta:
        db_table = 'checkout_order_item_db'
        ordering = ['-date_created', '-date_updated']
        get_latest_by = ['-date_created', '-date_updated']
        verbose_name_plural = 'panier'

    def __str__(self):
        return '{product_name}'.format(
            product_name=self.product.name
        )

    @property
    def total(self):
        return self.quantity * self.product.price

    def get_product_price(self):
        return '{product_price} Fr'.format(product_price=str(self.product.price))
    get_product_price.short_description='prix unitaire'

    def get_product_name(self):
        return '{product_name}'.format(product_name=str(self.product.name))
    get_product_name.short_description='produit'

    def get_phone_number(self):
        return '{phone}'.format(phone=str(self.product.user.phone))
    get_phone_number.short_description='N° de téléphone'

    def get_store_product(self):
        return '{product_store} | {store_phone}'.format(
            product_store=str(self.product.user.store),
            store_phone=self.get_phone_number())
    get_store_product.short_description='boutique'

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    # cout total apres commission
    def total_order(self):
        total = self.order.total_seller_order() - self.order.get_cost()
        return total


from django.dispatch import receiver
@receiver(models.signals.pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_order_id_generator(instance)
