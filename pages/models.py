# pages.models.py

from django.db import models
from django.utils import timezone

from category.models import Category

from core.utils import upload_image_path


NULL_AND_BLANK = {'null': True, 'blank': True}

class Annonce(object):
    link_to = models.SlugField(
        verbose_name='lien',
        max_length=100
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=upload_image_path,
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True   


class Promotion(Annonce):
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        verbose_name='promotion',
        **NULL_AND_BLANK
    )
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name='date de creation',
        default=timezone.now
    )
    
    def __str__(self):
        return f"{self.name}: {self.active}"


class Subscribe(models.Model):
    email = models.EmailField(
        verbose_name='email',
        **NULL_AND_BLANK
    )
    timestamp = models.DateTimeField(
        verbose_name="date",
        default=timezone.now
    )

    class Meta:
        verbose_name_plural = 'abonnement'

    def __str__(self):
        return self.email


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
    )
    message = models.TextField(
        verbose_name='message',
        **NULL_AND_BLANK
    )
    timestamp = models.DateTimeField(
        verbose_name="date",
        default=timezone.now
    )

    def __str__(self):
        return f"{self.full_name}: {self.email} - {self.phone}"

    class Meta:
        verbose_name_plural = 'message'
