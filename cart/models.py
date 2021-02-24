# cart.models.py

from django.db import models

from catalogue.models import Product

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
        db_table = 'cart_items_db'
        index_together = (('cart_id',),)
        ordering = ('-created_at', '-updated_at', '-cart_id')
        get_latest_by = ('-created_at', '-updated_at', '-cart_id')
        verbose_name_plural = 'panier'

    def __str__(self):
        return "{product}".format(product=self.product)

    def total(self):
        return self.quantity * self.product.price

    @property
    def price(self):
        return self.product.price

    def get_shop_name(self):
        return '{}'.format(self.product.user.store)
    get_shop_name.short_description='magasin'

    def get_product_name(self):
        return '{}'.format(str(self.product.name))
    get_product_name.short_description='nom du produit'

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        """
        called when a POST request comes in for a Product
        instance already in the shopping cart
        """
        self.quantity = self.quantity + int(quantity)
        self.save()
