# pages.models.py

from PIL import Image

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from core import utils
from catalogue.models import Product


NULL_AND_BLANK = {'null': True, 'blank': True}


class Testimonial(models.Model):
    full_name = models.CharField(
        max_length=120,
        verbose_name='nom & prénoms',
        help_text='Entrer le nom et prénoms du client'
    )
    status_client = models.CharField(
        max_length=120,
        verbose_name='Statut (entrepreneur/boutique/etc)',
        help_text='Entrer le statut du client',
        **NULL_AND_BLANK
    )
    message = models.TextField(
        verbose_name='message',
        help_text='Entrer le message du client'
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to='testimonial_image/',
        **NULL_AND_BLANK
    )
    created_at = models.DateField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='date',
    )
    activate_at = models.BooleanField(
        default=False,
        verbose_name='actif',
        help_text='rendre visible cet témoignage ?'
    )

    class Meta:
        db_table = 'testimonial_db'
        ordering = ['-created_at',]
        get_latest_by = ['-created_at',]
        verbose_name_plural = 'Témoignage'


class Promotion(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="store",
        limit_choices_to={
            'is_seller': True
        },
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='produit',
        limit_choices_to={
            'user__is_seller': True,
            'is_active': True
        },
        help_text="Choisir un produit à mettre en promotion"
    )
    name = models.CharField(
        max_length=120,
        verbose_name='titre de la promotion',
        help_text="Définir le titre de la promotion"
    )
    slug = models.SlugField(
        verbose_name='lien',
        blank=True, unique=True,
        help_text="lien auto-généré"
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=utils.upload_promotion_image_path,
        **NULL_AND_BLANK
    )
    active = models.BooleanField(
        verbose_name='promotion active ?',
        default=False,
        help_text="Cette promotion est active ?"
    )
    created_at = models.DateField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='date de creation',
    )

    class Meta:
        db_table = 'promotion_db'
        ordering = ['-created_at',]
        get_latest_by = ['-created_at',]
        verbose_name_plural = 'promotions'
        indexes = [models.Index(fields=['id'], name='id_promotion'),]

    def __str__(self):
        return f"{self.name}"

    def has_changed(instance, field):
        """
        Returns true if a field has changed in a model
        May be used in a model.save() method.
        """
        if instance.pk is not None:
            return True
        Klass = instance.__class__
        old = Klass.objects.filter(pk=instance.pk).exists()
        return not getattr(instance, field) == old

    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        if self.has_changed('image'):
            img = Image.open(self.image.path)
            if img.height > 399 and img.width > 1650: 
                output_size = (399, 1650) 
                img.thumbnail(output_size)
                img.convert('RGB') 
                img.save(self.image.path)

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return "https://via.placeholder.com/180"
        return self.image

    def show_image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.get_image_url()}" height="50"/>')
        else:
            return "https://via.placeholder.com/50"

    @admin.display(description="boutique")
    def get_store(self):
        return self.user.store

    def get_status(self):
        if self.active:
            return "Active"
        return "Désactivé"

    def get_absolute_url(self):
        return reverse(
            'promotion:promotion_detail', kwargs={'slug': str(self.slug)}
        )

    def get_update_promo_url(self):
        return reverse(
            'seller:promotion_update', kwargs={'slug': str(self.slug)}
        )

    def get_delete_promo_url(self):
        return reverse(
            'seller:promotion_delete', kwargs={'slug': str(self.slug)}
        )


class Contact(models.Model):
    full_name = models.CharField(
        verbose_name='Nom & prénoms',
        max_length=150,
        **NULL_AND_BLANK
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=150
    )
    phone = models.CharField(
        verbose_name='téléphone',
        max_length=150
    )
    subject = models.CharField(
        max_length=150,
        verbose_name='sujet de la requete',
    )
    company = models.CharField(
        verbose_name="entreprise",
        max_length=150,
        **NULL_AND_BLANK
    )
    message = models.TextField(
        verbose_name='message',
    )
    timestamp = models.DateTimeField(
        verbose_name="date",
        default=timezone.now
    )

    def __str__(self):
        return f"{self.full_name}: {self.email} - {self.phone}"

    class Meta:
        db_table = 'contact_db'
        ordering = ['-timestamp',]
        get_latest_by = ['-timestamp',]
        verbose_name_plural = 'messages'


@receiver([models.signals.pre_save], sender=Promotion)
def promotion_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = utils.unique_slug_generator(instance)
