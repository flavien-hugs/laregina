# checkout.models.py

import decimal
import random
import string
import datetime
from django.db import models
from django.urls import reverse

from core import settings
from core.utils import unique_key_generator

from cart.models import CartItem
from catalogue.models import Product

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
        blank_label='Sélection un pays',
        verbose_name='pays/région',
        multiple=False
    )
    shipping_adress = models.CharField(
        verbose_name='votre situation géographique',
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

    # status de chaque commande

    SUBMITTED = 'Soumis'
    PROCESSED = 'En cours de livraison'
    SHIPPED = 'Commande reçue'
    CANCELLED = 'Commande annulée'

    # ensemble de statuts d'ordre possibles

    ORDER_STATUSES = (
        (SUBMITTED, 'Soumis'),
        (PROCESSED, 'Commande en cours de livraison'),
        (SHIPPED, 'Commande reçue'),
        (CANCELLED, 'Commande annulée'),
    )

    status = models.CharField(
        verbose_name='status',
        max_length=26,
        choices=ORDER_STATUSES,
        default=SUBMITTED
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        verbose_name='client',
        **NULL_AND_BLANK
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

    class Meta:
        verbose_name_plural = 'commande'
    
    def __str__(self):
        return '#{transaction_id}'.format(
            transaction_id=self.transaction_id)

    def short_name(self):
        return '{first_name}'.format(
            first_name=self.shipping_first_name
        )

    def full_name(self):
        return '{short_name} {last_name}'.format(
            short_name=self.short_name(),
            last_name=self.shipping_last_name
        )

    def shipping_delivery(self):
        return '{shipping_city}, {shipping_adress}'.format(
            shipping_country=self.shipping_country.name,
            shipping_city=self.shipping_city,
            shipping_adress=self.shipping_adress
        )

    def save(self, *args, **kwargs):
        self.generate(8)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.transaction_id = 'LC-{}'.format(today + ''.join(random_carac))

    @property
    def total(self):
        total = decimal.Decimal('0')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total + 1500

    def total_seller_order(self):
        total = decimal.Decimal('0')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    def total_order(self):
        total = decimal.Decimal('0')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        commission = total * decimal.Decimal(0.05) 
        return int(total - commission)


    def order_items(self):
        return OrderItem.objects.filter(order=self)

    def store(self):
        return self.user.store
    store.short_description='magasin'
    
    def get_absolute_url(self):
        return reverse('seller:order_detail', kwargs={'pk': int(self.id)})


class OrderItem(models.Model):
    
    """
    classe modèle pour le stockage de chaque instance
    de produit commander dans chaque commande
    """

    product = models.ForeignKey(
        Product,
        models.SET_NULL,
        null=True,
        verbose_name='produit'
    )
    quantity = models.IntegerField(
        verbose_name='quantité',
        default=1
    )
    order = models.ForeignKey(
        Order,
        models.CASCADE,
        verbose_name='commande'
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
        return '{product_name} | {store}'.format(
            product_name=self.product.name,
            store=self.product.user.store
        )

    @property
    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name

    def store(self):
        return self.product.user.store
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()


from django.dispatch import receiver
@receiver(models.signals.pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_order_id_generator(instance)