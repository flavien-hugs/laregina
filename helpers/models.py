# common.models.py

from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator

from phonenumber_field.modelfields import PhoneNumberField
from .constants import COUNTRY_CHOICES, DEFAULT_COUNTRY_CHOICES

NULL_AND_BLANK = {"null": True, "blank": True}


class BaseTimeStampModel(models.Model):

    created_at = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name="date de création"
    )
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True

    @admin.display(description="date d'ajout")
    def date(self):
        return self.created_at.date()


class ModelSlugMixin(models.Model):

    slug = models.SlugField(
        max_length=225,
        unique=True,
        verbose_name="URL de la boutique",
        help_text="Automatiquement formé à partir du nom.",
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class PublishedMixin(models.Model):

    published = models.DateTimeField(
        default=timezone.now,
        auto_now_add=False,
        auto_now=False,
        verbose_name="date de publication",
        help_text="Programmé la date et l'heure de la formation.",
    )

    class Meta:
        abstract = True

    @admin.display(description="publié le")
    def date(self):
        return self.published.date()


class BaseOrderInfo(models.Model):

    email = models.EmailField(verbose_name="adresse de messagerie", max_length=50)
    shipping_first_name = models.CharField(verbose_name="nom de famille", max_length=50)
    shipping_last_name = models.CharField(verbose_name="prénom", max_length=50)
    phone = PhoneNumberField("numéro de téléphone")

    phone_two = PhoneNumberField(
        verbose_name="téléphone supplémentaire (facultatif)", blank=True
    )
    shipping_city = models.CharField(verbose_name="ville", max_length=50)
    shipping_country = models.CharField(
        max_length=25,
        verbose_name="Pays/Région",
        choices=COUNTRY_CHOICES,
        default=DEFAULT_COUNTRY_CHOICES,
    )
    shipping_adress = models.CharField(
        verbose_name="situation géographique", max_length=50
    )
    shipping_zip = models.CharField(
        verbose_name="adresse postal (facultatif)", max_length=10, **NULL_AND_BLANK
    )
    note = models.TextField(
        verbose_name="note de commande (facultatif)", max_length=120, **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class ApplyDiscountModel(models.Model):
    user = models.ForeignKey(
        to="accounts.User",
        on_delete=models.CASCADE,
        verbose_name="store",
        limit_choices_to={"is_seller": True},
    )
    products = models.ManyToManyField(
        to="catalogue.Product",
        verbose_name="produits",
        help_text="Choisir des produits",
    )
    is_active = models.BooleanField(
        verbose_name="Activé/Désactivé", default=False, help_text="Activé/Désactivé ?"
    )

    class Meta:
        abstract = True

    @admin.display(description="boutique")
    def get_store(self):
        return self.user.store

    def get_status(self):
        if self.is_active:
            return "Active"
        return "Désactivé"

    @admin.display(description="produits")
    def get_products(self):
        return self.products.all()

    @admin.display(description="nombre de produits")
    def get_products_count(self):
        return len(self.get_products())
