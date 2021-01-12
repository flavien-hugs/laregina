# cart.managers.py

from django.db import models
from django.db.models import Q
from django.utils import timezone


class CartQuerySet(models.query.QuerySet):
    def total_price(self):
        return sum([x.total_price() for x in self.all()])

    def order_by_shop(self):
        cart = []
        class Cart:
            pass

        for item in self.all():
            flag = True
            user = item.product.user
            for x in cart:
                if x.user == user:
                    flag = False
            if flag:
                cart = Cart()
                cart.user = user
                cart.carts = self.filter(product__user=cart.user)
                cart.price = sum([x.total_price() for x in cart.carts])

                shops.append(shop)
        return shops


class CartManager(models.Manager):

    def get_queryset(self):
        return CataloqueQuerySet(self.model, using=self._db)