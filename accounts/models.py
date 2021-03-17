# accounts.models.py

import random
import string
import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from category.models import Category
from checkout.models import BaseOrderInfo
from accounts.managers import UserManager

from core.utils import upload_image_path

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}


class User(BaseOrderInfo, AbstractBaseUser, PermissionsMixin):

    CIVILITY_CHOICES = (
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('Mlle', 'Mlle'),
    )

    civility = models.CharField(
        max_length=4,
        default="M.",
        choices=CIVILITY_CHOICES,
        verbose_name='civilité',
    )
    store_id = models.CharField(
        max_length=50,
        verbose_name='ID BOUTIQUE',
        unique=True,
        **NULL_AND_BLANK
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email',
        error_messages={
            'unique': "Un utilisateur disposant de ce courriel existe déjà."
        }
    )
    store = models.CharField(
        max_length=80,
        verbose_name='boutique',
        unique=True,
        error_messages={
            'unique': "Un magasin disposant de ce nom existe déjà."
        },
    )
    store_description = models.TextField(
        max_length=254,
        verbose_name='description de la boutique',
        **NULL_AND_BLANK
    )
    facebook = models.URLField(
        verbose_name='compte facebook',
        max_length=250,
        **NULL_AND_BLANK
    )
    twitter = models.URLField(
        verbose_name='compte twitter',
        max_length=250,
        **NULL_AND_BLANK
    )
    linkedin = models.URLField(
        verbose_name='compte linkedin',
        max_length=250,
        **NULL_AND_BLANK
    )
    instagramm = models.URLField(
        verbose_name='compte instagramm',
        max_length=250,
        **NULL_AND_BLANK
    )
    is_seller = models.BooleanField(
        default=False,
        verbose_name='statut vendeur',
    )
    is_staff = models.BooleanField(
        verbose_name='statut équipe',
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name='statut administrateur',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True
    )
    last_login = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date de derniere connexion',
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date d'inscription",
    )
    slug = models.SlugField(
        blank=True,
        verbose_name="URL de la boutique",
        help_text="lien vers la boutique"
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = 'accounts'
        db_table = 'accounts_db'
        index_together = (('email',),)
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'vendeur(s)'

    def __str__(self):
        return '{store} | {name}'.format(
            store=self.store.upper(),
            name=self.shipping_last_name.capitalize()
        )

    def save(self, *args, **kwargs):
        if self.is_seller:
            self.generate(6)

        if not self.slug:
            self.slug = slugify(self.store)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.store_id = 'LRG-{}'.format(today + ''.join(random_carac))

    def get_fullname(self):
        if self.civility and self.shipping_first_name:
            full_name = '{civility} {shipping_first_name}'.format(
                civility=str(self.civility),
                shipping_first_name=str(self.shipping_first_name)
            )
            return full_name.strip()
        return self.email

    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ?"
        return self.is_superuser

    def has_module_perms(self, app_label):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ? ?"
        return self.is_superuser

    def get_update_url(self):
        return reverse('seller:update', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('store_detail_view', kwargs={'slug': self.slug})


class GuestCustomer(BaseOrderInfo):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email',
        error_messages={
            'unique': "Un utilisateur disposant de ce courriel existe déjà."
        }
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'accounts'
        db_table = 'accounts_buyer_db'
        index_together = (('email',),)
        ordering = ('-created_at', '-active')
        get_latest_by = ('-created_at', '-active')
        verbose_name_plural = 'acheteur(s)'

    def __str__(self):
        return '{email}({created})'.format(email=self.email, created=self.active)

    def get_fullname(self):
        if self.shipping_first_name and self.shipping_last_name:
            full_name = '{shipping_last_name} {shipping_first_name}'.format(
                shipping_last_name=self.shipping_last_name,
                shipping_first_name=self.shipping_first_name
            )
            return full_name.strip()
        return self.email
