# order.models.py

import random
import string
import datetime

from django.db import models
from django.contrib.auth import get_user_model

from cart.models import CartItem

# User Manager
User = get_user_model()

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'blank': True, 'max_digits': 50, 'decimal_places': 2}


class Order(models.Model):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='user',
    )
    track_order = models.CharField(verbose_name='ID de la commande', max_length=10, blank=True)
    cart = models.ManyToManyField(CartItem, verbose_name='panier')
    payed = models.FloatField(verbose_name='montant', default=0.0, blank=True)
    payed_date = models.DateTimeField(verbose_name='date de paiement', **NULL_AND_BLANK)
    is_payed = models.BooleanField(verbose_name='paiement effectué', default=False)

    sent_date = models.DateTimeField(verbose_name="date d'expédition", **NULL_AND_BLANK)
    delivered_date =models.DateTimeField(verbose_name='date de la livraison', **NULL_AND_BLANK)

    status = models.CharField(verbose_name='status', max_length=100)
    is_direct_pay = models.BooleanField(verbose_name='paiement direct', default=False)

    cancelReason = models.TextField(verbose_name="motifs d'annulation", **NULL_AND_BLANK)
    is_canceled = models.BooleanField(verbose_name='annulé', default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.track_order

    def price(self):
        return self.cart.all().get_product_price()

    def save(self, *args, **kwargs):
        self.generate(10)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.track_order = today + ''.join(random_carac)

    class Meta:
        ordering = ['-timestamp', '-modify_date']
        index_together = ('track_order',)
        verbose_name_plural = 'commandes'


class Address(models.Model):
    country = models.CharField(verbose_name='pays', max_length=50)
    region = models.CharField(verbose_name='région', max_length=50, blank=True)
    city = models.CharField(verbose_name='ville', max_length=50, blank=True)
    street = models.CharField(verbose_name='quartier/rue', max_length=200)
    zip_code = models.CharField(verbose_name='code postal', max_length=20, blank=True)
    phone_1 = models.CharField(verbose_name='téléphone', max_length=20)
    phone_2 = models.CharField(verbose_name='numéro de téléphone 2', max_length=20, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'adresse de livraison'
