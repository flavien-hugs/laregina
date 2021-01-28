# cart.models.py

from decimal import Decimal
from django.db import models
from django.conf import settings
from django.dispatch import receiver

from catalogue.models import Product

# User Manager
User = settings.AUTH_USER_MODEL
NULL_AND_BLANK = {'null': True, 'blank': True}
DECIMAFIELD_OPTION = {'default': 0, 'max_digits': 50, 'decimal_places': 2}


class CartItem(models.Model):
    cart_id = models.CharField(
        verbose_name='ID PANIER',
        max_length=50,
        db_index=True
    )
    product = models.ForeignKey(
        Product,
        models.CASCADE,
        verbose_name='produit',
        unique=False
    )
    quantity = models.PositiveIntegerField(verbose_name='quantité', default=1)
    created_at = models.DateTimeField(verbose_name='date d\'ajout', auto_now=True)
    updated_at = models.DateTimeField(
        verbose_name='date de mise à jour',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        db_table = 'cart_items'
        ordering = ['-updated_at', '-created_at']
        verbose_name_plural = 'panier'

    def __str__(self):
        return "{product}".format(product=self.product)

    @property
    def total(self):
        return self.quantity * self.product.price

    @property
    def price(self):
        return self.product.price

    @property
    def name(self):
        return self.product.name
    
    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()

    def get_absolute_url(self):
        return self.product.get_absolute_url()


# class Cart(models.Model):
#     user = models.ForeignKey(
#         User,
#         models.CASCADE,
#         related_name='cart',
#         verbose_name='client',
#         null=True
#     )
#     total = models.DecimalField(verbose_name='prix total', **DECIMAFIELD_OPTION)
#     created_at = models.DateTimeField(
#         verbose_name='date d\'ajout',
#         auto_now_add=True,
#         auto_now=False
#     )
#     updated_at = models.DateTimeField(
#         verbose_name='date de mise à jour',
#         auto_now_add=False,
#         auto_now=True
#     )
#     active = models.BooleanField(verbose_name='actif', default=True)

#     def __str__(self):
#         return str(self.id)

#     class Meta:
#         ordering = ['total', '-updated_at']
#         verbose_name_plural = 'parnier'

#     @property
#     def get_shop_name(self):
#         return self.user.store

#     def update_total(self):
#         print("updating...")
#         total = 0
#         product_item = self.cart_items.all()
#         for item in product_item:
#             total += item.price
#         self.total = "{total}.2f".format(total=total)
#         self.save()


# @receiver(models.signals.pre_save, sender=CartItem)
# def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
#     quantity = instance.quantity
#     if quantity >= 1:
#         price = instance.product.get_sale_price()
#         item_total = Decimal(quantity) * Decimal(price)
#         instance.item_total = item_total


# @receiver([models.signals.post_save, models.signals.post_delete], sender=CartItem)
# def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
#     instance.cart.update_subtotal()


# @receiver([models.signals.pre_save], sender=Cart)
# def update_cart_total(sender, instance, **kwargs):
#     totals = Decimal(instance.total)
#     total = round(totals, 2)
#     instance.total = "%.2f" %(total)
