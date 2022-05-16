# voucher.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import(
	MinValueValidator,
	MaxValueValidator
)

from catalogue.models import Product
from voucher.managers import VoucherManager
from helpers.models import BaseTimeStampModel

User = settings.AUTH_USER_MODEL
validators = [MinValueValidator(0), MaxValueValidator(100)]


class Voucher(BaseTimeStampModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_seller': True},
        verbose_name='vendeur',
        help_text="magasin en charge de la vente."
    )
    products = models.ManyToManyField(
        to=Product,
        verbose_name="produits"
    )
    discount = models.IntegerField(
        verbose_name="pourcentage de réduction",
        validators=validators
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="valide oui/non ?"
    )

    objects = VoucherManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "réductions produits"
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return f"{self.discount}% de réductions"

    def get_status(self):
        if self.is_active:
            return "Active"
        return "Désactivé"

    def get_update_voucher_url(self):
        return reverse(
            'seller:voucher_update', kwargs={'pk': str(self.pk)}
        )

    def get_delete_voucher_url(self):
        return reverse(
            'seller:voucher_delete', kwargs={'pk': str(self.pk)}
        )

    def voucher_validate(self):
    	return f"Valable de {self.valid_from.date()} à {self.valid_to.date()}"

    @admin.display(description="produits")
    def get_products(self):
        return self.products.all()

    @admin.display(description="nombre de produits")
    def get_products_count(self):
        return len(self.get_products())

    @admin.display(description="prix réduit")
    def get_price(self):
        single_product_price = [
            ((obj.price * self.discount)/100) for obj in self.get_products()
        ]
        return single_product_price

    @admin.display(description="% de réduction")
    def get_discount(self) -> str:
        return f"{self.discount}%"
