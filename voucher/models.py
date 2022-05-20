# voucher.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import(
    MinValueValidator, MaxValueValidator
)

from catalogue.models import Product
from helpers.models import BaseTimeStampModel, ApplyDiscountModel


validators = [MinValueValidator(0), MaxValueValidator(100)]


class Voucher(BaseTimeStampModel, ApplyDiscountModel):
    
    discount = models.IntegerField(
        verbose_name="pourcentage de réduction",
        validators=validators
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "réductions produits"
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return f"{self.discount}% de réductions"

    @admin.display(description="prix réduit")
    def get_price(self):
        single_product_price = [
            ((obj.price * self.discount)/100) for obj in self.get_products()
        ]
        return single_product_price

    @admin.display(description="% de réduction")
    def get_discount(self) -> str:
        return f"{self.discount}%"

    def get_update_voucher_url(self):
        return reverse(
            'seller:voucher_update',
            kwargs={'pk': str(self.pk)}
        )

    def get_delete_voucher_url(self):
        return reverse(
            'seller:voucher_delete',
            kwargs={'pk': str(self.pk)}
        )
