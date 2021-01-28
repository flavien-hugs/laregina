# order.models.py

import random
import string
import datetime

from django.db import models
from django.contrib.auth import get_user_model

from cart.models import CartItem
from catalogue.models import Product
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# User Manager
User = get_user_model()

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'blank': True, 'max_digits': 50, 'decimal_places': 2}


class BaseOrderInfo(models.Model):

    class Meta:
        abstract = True

    # contact info

    email = models.EmailField(verbose_name='adresse email', max_length=50)
    phone = PhoneNumberField('numéro de téléphone')

    # shipping information

    shipping_first_name = models.CharField(verbose_name='nom de famille', max_length=50)
    shipping_last_name = models.CharField(verbose_name='prénom', max_length=50)
    shipping_address = PhoneNumberField(
        verbose_name='numéro de téléphone WhatsApp',
        blank=True,
        help_text="+225xxxxxxxx"
    )
    shipping_city = models.CharField(verbose_name='ville', max_length=50)
    shipping_country = CountryField(blank_label='Pays de résidence', verbose_name='pays')
    shipping_zip = models.CharField(verbose_name='adresse postal (optionnel)', max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(BaseOrderInfo):

    # status de chaque commande

    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    # ensemble de statuts d'ordre possibles

    ORDER_STATUSES = (
        (SUBMITTED, 'Soumis'),
        (PROCESSED, 'Traitée'),
        (SHIPPED, 'Expédié'),
        (CANCELLED, 'Annulé'),
    )

    # info order

    date = models.DateTimeField(verbose_name='date de la commade', auto_now_add=True)
    status = models.IntegerField(
        verbose_name='status de le commande',
        choices=ORDER_STATUSES,
        default=SUBMITTED
    )
    last_updated = models.DateTimeField(
        verbose_name='derniere modification',
        auto_now=True
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        verbose_name='client'
    )
    transaction_id = models.CharField(
        verbose_name='id de la commande',
        max_length=20
    )
    ip_address = models.CharField(
        verbose_name='adresse ip',
        max_length=50
    )
    emailing = models.BooleanField(verbose_name='activer les offres', default=False)

    class Meta:
        verbose_name_plural = 'commande'
    
    def __str__(self):
        return ('Order #{ID}').format(ID=self.id)

    @property
    def full_name(elf):
        return '{first_name} {last_name}'.format(
            first_name=self.shipping_first_name,
            last_name=self.shipping_last_name)

    def save(self, *args, **kwargs):
        self.generate(12)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.transaction_id = today + ''.join(random_carac)
    
    @property
    def total(self):
        total = decimal.Decimal('0')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total
    
    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'transaction_id': self.transaction_id})


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
    price = models.DecimalField(
        verbose_name='coût total',
        max_digits=9,
        decimal_places=2
    )
    order = models.ForeignKey(
        Order,
        models.CASCADE,
        verbose_name='commande'
    )

    class Meta:
        verbose_name_plural = 'panier'

    def __str__(self):
        return '{product_name} | {store}'.format(
            product_name=self.product.name,
            store=self.product.user.store
        )
    
    @property
    def total(self):
        return self.quantity * self.price
    
    @property
    def name(self):
        return self.product.name
    
    @property
    def store(self):
        return self.product.user.store
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()