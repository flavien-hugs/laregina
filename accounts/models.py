# accounts/models.py

import math
import random
import string
import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from category.models import Category
from accounts.managers import UserManager
from tagulous.models import SingleTagField
from core.utils import generate_key, upload_image_path


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}


class User(AbstractBaseUser, PermissionsMixin):

    """ 
        Un modèle d'utilisateur complet avec des autorisations compatibles
        avec l'administrateur qui utilise un champ de courrier électronique
        complet comme nom d'utilisateur. Email et mot de passe sont requis.
        Les autres champs sont facultatifs. 
    """

    CIVILITY_CHOICES = (('M.', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle'),)
    store_id = models.CharField(max_length=120, verbose_name='ID STORE', unique=True, blank=True)
    email = models.EmailField(verbose_name='email', max_length=254, unique=True,
        error_messages={'unique': "Un utilisateur disposant de ce courriel existe déjà.",})
    civility = models.CharField(verbose_name='civilité', max_length=4, choices=CIVILITY_CHOICES, default="Mr")
    name = models.CharField(verbose_name="nom & prénoms", max_length=120)
    store = models.CharField(verbose_name='boutique', max_length=254, **NULL_AND_BLANK)
    phone_number = PhoneNumberField('numéro de téléphone', help_text="+225xxxxxxxx",)
    whatsapp_number = PhoneNumberField(
        verbose_name='numéro de téléphone WhatsApp',
        blank=True,
        help_text="+225xxxxxxxx"
    )
    country = CountryField(blank_label='choisir le pays', **NULL_AND_BLANK)
    city = models.CharField(verbose_name='ville', max_length=250, **NULL_AND_BLANK)
    address = models.CharField(verbose_name='adresse', max_length=250, **NULL_AND_BLANK)
    store_description = models.TextField('description de la boutique', max_length=2000, **NULL_AND_BLANK)
    logo = models.ImageField(verbose_name='logo', upload_to=upload_image_path, **NULL_AND_BLANK)
    facebook = models.URLField(verbose_name='lien facebook', max_length=250, **NULL_AND_BLANK)
    twitter = models.URLField(verbose_name='lien twitter', max_length=250, **NULL_AND_BLANK)
    linkedin = models.URLField(verbose_name='lien linkedin', max_length=250, **NULL_AND_BLANK)
    instagramm = models.URLField(verbose_name='lien instagramm', max_length=250, **NULL_AND_BLANK)
    is_staff = models.BooleanField(verbose_name='statut équipe', default=False)
    is_superuser = models.BooleanField(verbose_name='statut administrateur', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_buyer = models.BooleanField(verbose_name='statut acheteur', default=False)
    is_seller = models.BooleanField(verbose_name='statut vendeur', default=False)
    last_login = models.DateTimeField(verbose_name='date de derniere connexion', auto_now_add=True)
    date_joined = models.DateTimeField(verbose_name="date d'inscription", auto_now_add=True)
    slug = models.SlugField("URL de la boutique", blank=True, help_text="lien vers la boutique")

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('-date_joined',)
        index_together = (('email',),)
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_seller:
            self.generate(8)

        if not self.slug:
            self.slug = slugify(self.store)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.store_id = today + ''.join(random_carac)

    def get_fullname(self):
        if self.civility and self.name:
            fullname = '{civility} {name}'.format(civility=self.civility, name=self.name)
            return fullname.strip()
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have permissions to view the app `app_label` ?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label` ?"
        return True

    def get_absolute_url(self):
        return reverse('store_detail_view', kwargs={'slug': self.slug})
