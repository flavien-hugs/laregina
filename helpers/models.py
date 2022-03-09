# common.models.py


from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


NULL_AND_BLANK = {'null': True, 'blank': True}


class BaseTimeStampModel(models.Model):

    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now,
        verbose_name="date de création"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @admin.display(description="date d'ajout")
    def date(self):
        return self.created_at.date()


class ModelSlugMixin(models.Model):

    slug = models.SlugField(
        editable=False,
        max_length=225, unique=True,
        verbose_name="URL de la boutique",
        help_text='Automatiquement formé à partir du nom.',
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class PublishedMixin(models.Model):

    published = models.DateTimeField(
        default=timezone.now,
        auto_now_add=False, auto_now=False,
        verbose_name='date de publication',
        help_text="Programmé la date et l'heure de la formation."
    )

    class Meta:
        abstract = True

    @admin.display(description="publié le")
    def date(self):
        return self.published.date()


class BaseOrderInfo(models.Model):

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
        blank_label='sélection un pays',
        verbose_name='pays/région',
        multiple=False
    )
    shipping_adress = models.CharField(
        verbose_name='situation géographique',
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

    class Meta:
        abstract = True
