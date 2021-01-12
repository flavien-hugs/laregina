# cart.models.py

from django.db import models
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.dispatch.dispatcher import receiver

from catalogue.models import Product

# User Manager
User = get_user_model()
DECIMAFIELD_OPTION = {'default': 0, 'max_digits': 50, 'decimal_places': 2}

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        related_name='cart',
        verbose_name='panier'
    )
    total = models.DecimalField(verbose_name='prix total', **DECIMAFIELD_OPTION)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['total', '-id', '-timestamp']
        verbose_name_plural = 'parnier'

    def get_total_price(self):
        price_total = sum(item.get_product_price() for item in self.cart_items.all())
        return price_total


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        models.CASCADE,
        related_name='cart_items',
        verbose_name='élément dans le panier du client'
    )
    product = models.ForeignKey(
        Product,
        models.SET_NULL,
        null=True,
        related_name='product',
        verbose_name='produit')
    quantity = models.PositiveIntegerField(verbose_name='quantité', default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['product__user', '-id', '-timestamp']
        verbose_name_plural = 'élément du panier'

    def __str__(self):
        return "{product}".format(product=self.product.name)

    @property
    def get_product_price(self):
        return self.product.price * self.quantity

    @property
    def get_shop(self):
        return self.product.user

    @property
    def name(self):
        return self.product.name
    
    @property
    def price(self):
        return self.product.get_sale_price()
    
    def augment_quantity(self, quantity):
        """ appelé lorsqu'une demande de POST arrive pour une instance de produit déjà dans le panier """
        self.quantity = self.quantity + int(quantity)
        self.save()

    # def get_absolute_url(self):
    #     return self.product.get_absolute_url()


@receiver([signals.post_save, signals.post_delete], sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    total_price = [item.product.get_price() for item in cart.cart_items.all()]
    cart.total = sum(total_price)
    cart.save()
