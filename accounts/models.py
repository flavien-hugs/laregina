# accounts.models.py

import random
import string
import datetime

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers import UserManager
from helpers.utils import(
    upload_image_logo_path, vendor_unique_slug_generator
)

from helpers.models import(
    BaseTimeStampModel, BaseOrderInfo, ModelSlugMixin
)

import phonenumbers

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}


class User(
    BaseOrderInfo, ModelSlugMixin, BaseTimeStampModel,
    AbstractBaseUser, PermissionsMixin):

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
    logo = models.ImageField(
        verbose_name="logo",
        upload_to=upload_image_logo_path,
        help_text="Ajouter le logo de votre boutique",

        **NULL_AND_BLANK
    )
    formatted_logo = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(150, 150)],
        format='PNG',
        options={'quality': 100}
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
        verbose_name_plural = 'boutiques'
        indexes = [models.Index(fields=['id'], name='id_index'),]


    def __str__(self):
        return f"{self.store.upper()} | {self.shipping_last_name.capitalize()}"

    def save(self, *args, **kwargs):
        if self.is_seller:
            self.generate(6)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.store_id = 'LRG-{}'.format(today + ''.join(random_carac))

    def get_fullname(self):
        if self.shipping_last_name and self.shipping_first_name:
            full_name = f"{self.shipping_last_name} {self.shipping_first_name}"
            return full_name.strip()
        return self.email

    def formatted_phone(self, country=None):
        return phonenumbers.parse(self.phone, country)

    @admin.display(description="compte verifié")
    def account_verified(self):
        from allauth.account.models import EmailAddress
        result = EmailAddress.objects.filter(email=self.email)
        if len(result):
            return result[0].verified
        return False

    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ?"
        return self.is_superuser

    def has_module_perms(self, app_label):
        "L'utilisateur a-t-il les permissions pour voir l'application `app_label` ? ?"
        return self.is_superuser

    def get_update_url(self):
        return reverse('seller:update', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('vendor:store_detail_view', kwargs={'slug': self.slug})

    def get_social_url(self):
        return reverse('seller:rs_update', kwargs={"slug": self.slug})

    @admin.display(description="logo")
    def get_vendor_logo(self):
        if self.logo:
            return mark_safe(f"<img src='{self.logo.url}' width='50' height='50'/>")
        return mark_safe("<img src='/static/img/default.jpeg' height='50'/>")

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/img/default.jpeg"

    def orders(self):
        from checkout.models import Order, OrderItem
        order = Order.objects.prefetch_related("status")\
            .filter(orders__product__user=self, status=Order.SHIPPED)
        order_item = OrderItem.objects\
            .prefetch_related("order")\
            .filter(models.Q(order__in=order))
        return order_item

    @admin.display(description="nombre de produits")
    def products(self):
        from catalogue.models import Product
        products = Product.objects.prefetch_related("user").filter(user=self)
        return products.count()

    def get_social_profile(self):
        return ProfileSocialMedia.objects.prefetch_related("user").filter(user=self)


class ProfileSocialMedia(BaseTimeStampModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        verbose_name="users"
    )
    facebook = models.URLField(
        verbose_name='compte facebook',
        max_length=250,
        help_text="Copier at coller le lien facebook de votre page ici.",
        **NULL_AND_BLANK
    )
    instagram = models.URLField(
        verbose_name='compte instagram',
        max_length=250,
        help_text="Copier at coller le lien instagram de votre page ici.",
        **NULL_AND_BLANK
    )

    class Meta:
        app_label = 'accounts'
        db_table = 'accounts_social_db'
        index_together = (('user',),)
        verbose_name_plural = 'profile reseaux sociaux'
        indexes = [models.Index(fields=['id'], name='id_rs_index'),]

    def __str__(self):
        return self.user.get_fullname()

    def get_facebook(self):
        return self.facebook

    def get_instagram(self):
        return self.instagram


class GuestCustomer(BaseOrderInfo, BaseTimeStampModel):

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email',
        error_messages={
            'unique': "Un utilisateur disposant de ce courriel existe déjà."
        }
    )
    active = models.BooleanField(default=True)

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
        if self.shipping_last_name and self.shipping_first_name:
            full_name = f"{self.shipping_last_name} {self.shipping_first_name}"
            return full_name.strip()
        return self.email


@receiver([models.signals.pre_save], sender=User)
def vendor_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = vendor_unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=User)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_image = Klass.objects.get(pk=instance.pk).logo
            if old_image and old_image.url != instance.logo.url:
                old_image.delete(save=False)
        except:
            pass
