# pages.models.py

from PIL import Image

from django.db import models
from django.utils import timezone

from category.models import Category
from core.utils import upload_promotion_image_path


NULL_AND_BLANK = {'null': True, 'blank': True}


class Annonce(models.Model):
    link_to = models.SlugField(
        verbose_name='lien',
        max_length=100
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=upload_promotion_image_path,
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


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


class Promotion(Annonce):
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        verbose_name='promotion',
        **NULL_AND_BLANK
    )
    title = models.CharField(
        max_length=120,
        verbose_name='Titre de la promotion'
    )
    active = models.BooleanField(
        verbose_name='promotion active ?',
        default=False
    )
    created_at = models.DateField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='date de creation',
    )

    class Meta:
        db_table = 'promotion_db'
        unique_together = ['link_to']
        index_together = (('link_to','title'),)
        ordering = ['-created_at',]
        get_latest_by = ['-created_at',]
        verbose_name_plural = 'promotion'

    def __str__(self):
        return f"{self.title}: {self.category.name}"

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
        return self.image


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
