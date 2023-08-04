import datetime
import logging
import random
import string

import phonenumbers
from accounts.managers import UserManager
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from helpers.models import BaseInfoMixin
from helpers.utils import upload_image_to
from helpers.models import BaseTimeStampModel
from helpers.utils import user_slug_generator

from . import constants

# from django.urls import reverse

logger = logging.getLogger(__name__)
NULL_AND_BLANK = {"null": True, "blank": True}
UNIQUE_AND_DB_INDEX = {"null": False, "unique": True, "db_index": True}
image_validators = [FileExtensionValidator(["jpeg", "jpg", "png"])]


class User(
    BaseInfoMixin,
    BaseTimeStampModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    published = True

    file_prepend = "upload/users/"

    gender = models.CharField(
        max_length=12,
        choices=constants.CIVILITY_CHOICES,
        default=constants.DEFAULT_CIVILITY_CHOICES,
        verbose_name="civilité",
    )
    user_id = models.CharField(
        max_length=6, verbose_name="user ID", unique=True, **NULL_AND_BLANK
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="email",
        error_messages={
            "unique": "Un utilisateur disposant de ce courriel existe déjà."
        },
    )
    description = models.TextField(
        max_length=254, verbose_name="description", **NULL_AND_BLANK
    )
    avatar = models.ImageField(
        verbose_name="avatar",
        upload_to=upload_image_to,
        validators=image_validators,
        **NULL_AND_BLANK,
    )
    is_customer = models.BooleanField(
        default=False,
        verbose_name="client",
    )
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    is_superuser = models.BooleanField(verbose_name="administrateur", default=False)
    is_active = models.BooleanField(verbose_name="active", default=True)
    last_login = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date de derniere connexion",
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.is_customer:
            self.generate(6)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime("%d%m%y")
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.user_id = "{}".format(today + "".join(random_carac))

    def formatted_phone(self, country=None):
        return phonenumbers.parse(self.phone, country)

    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ?"
        return self.is_superuser

    def has_module_perms(self, app_label):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ? ?"
        return self.is_superuser

    @admin.display(description="avatar")
    def get_user_avatar(self):
        if self.avatar:
            return mark_safe(f"<img src='{self.avatar.url}!r' width='50' height='50'/>")
        return mark_safe("<img src='/static/img/default.jpeg' height='50'/>")

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/img/default.jpeg"

    def orders(self):
        from checkout.models import Order, OrderItem

        order = Order.objects.prefetch_related("status").filter(
            orders__product__user=self, status=Order.SHIPPED
        )
        order_item = OrderItem.objects.prefetch_related("order").filter(
            models.Q(order__in=order)
        )
        return order_item

    @classmethod
    def filter_by_id(cls, pk):
        return cls.objects.filter(pk=pk).get()

    @classmethod
    def filter_by_email(cls, email):
        return cls.objects.filter(email=email)


class DistributorCustomer(BaseInfoMixin, BaseTimeStampModel):
    note = email = shipping_zip = None
    shipping_country = shipping_adress = shipping_first_name = shipping_last_name = None

    gender = models.CharField(
        max_length=12,
        choices=constants.CIVILITY_CHOICES,
        default=constants.DEFAULT_CIVILITY_CHOICES,
        verbose_name="Civilité",
    )
    fullname = models.CharField(verbose_name="Nom & Prénoms", max_length=50)
    birth_date = models.DateField(verbose_name="Votre date de naisssance", null=True)
    marital_status = models.CharField(
        max_length=100,
        choices=constants.MARITAL_STATUS_CHOICES,
        default=constants.DEFAULT_MARITAL_STATUS,
        verbose_name="Situation matrimoniale",
    )
    nationnality = models.CharField(max_length=80, verbose_name="Nationalité")
    level_of_education = models.CharField(
        max_length=100,
        verbose_name="Niveau d'étude",
        choices=constants.LEVEL_OF_EDUCATION_CHOICES,
        default=constants.DEFAULT_LEVEL_OF_EDUCATION_CHOICES,
    )
    profession = models.CharField(max_length=100, verbose_name="Profession", null=True)
    commune = models.CharField(max_length=180, verbose_name="Commune", null=True)
    district = models.CharField(max_length=180, verbose_name="Quartier", null=True)
    local_market = models.CharField(
        max_length=100, verbose_name="Marché à proximité de vous"
    )
    id_card_number = models.CharField(
        max_length=50,
        verbose_name="Numéro de votre pièce d'identité (CNI, PASSEPORT, PERMIS)",
        null=True,
    )
    delivery_id = models.CharField(
        max_length=6, unique=True, verbose_name="ID Distributeur", **NULL_AND_BLANK
    )
    active = models.BooleanField(verbose_name="Activer le compte", default=False)

    class Meta:
        ordering = ["-created_at", "-active"]
        verbose_name_plural = "distributeurs"

    def __str__(self):
        return f"{self.delivery_id} - {self.get_delivery_location()} - {self.get_fullname()}"

    @admin.display(description="Info supp. livreur")
    def get_delivery_location(self):
        return f"{self.commune} - {self.district} - {self.local_market}"

    @admin.display(description="Nom & prénoms")
    def get_fullname(self):
        if self.fullname:
            full_name = f"{self.gender} {self.fullname} ({self.phone})"
            return full_name.strip()
        return self.phone

    @admin.display(boolean=True)
    def born_in_nineties(self):
        return 1992 <= self.birth_date.year < 2004

    def save(self, *args, **kwargs):
        if self.delivery_id is None:
            self.generate_delivery_id(6)
        super().save(*args, **kwargs)

    def generate_delivery_id(self, nb_carac):
        today = datetime.date.today().strftime("%d%m%y")
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.delivery_id = "{}".format(today + "".join(random_carac))


@receiver([models.signals.pre_save], sender=User)
def user_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug != user_slug_generator(instance):
        instance.slug = user_slug_generator(instance)


@receiver([models.signals.pre_save], sender=User)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_image = Klass.objects.get(pk=instance.pk).avatar
            if old_image and old_image.url != instance.avatar.url:
                old_image.delete(save=False)
        except Klass.DoesNotExist:
            logger.error("The Klass does not exist with that ID")
