# pages.models.py

from django.core.validators import(
    MinValueValidator, MaxValueValidator
)
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

from catalogue.models import Product
from pages.managers import PageModelManager
from helpers.utils import(
    upload_promotion_image_path,
    upload_campign_image_path,
    unique_slug_generator
)
from helpers.models import(
    BaseTimeStampModel, ModelSlugMixin,
    ApplyDiscountModel
)

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


validate_video = [
    FileExtensionValidator(
        allowed_extensions=[
            'mp4', 'webm', 'flv', 'mov',
            'ogv' ,'3gp' ,'3g2' ,'wmv' ,
            'mpeg' ,'flv' ,'mkv' ,'avi'
        ]
    )
]
validators = [MinValueValidator(0), MaxValueValidator(100)]
NULL_AND_BLANK = {'null': True, 'blank': True}


class HomePage(BaseTimeStampModel):

    ELECT = 0
    MARKET = 1
    COMBIN = 2
    DEFAULT_PAGE = ELECT

    PAGE_CHOICES = (
        (ELECT, "Page par défaut"),
        (MARKET, "Page Supermarché"),
        (COMBIN, "Page Combinée"),
    )

    page = models.PositiveIntegerField(
        verbose_name='Page',
        choices=PAGE_CHOICES,
        default=DEFAULT_PAGE
    )

    class Meta:
        verbose_name_plural = "Accueil page"
        indexes = [models.Index(fields=['id'],)]

    def __str__(self) -> str:
        return f"Page active pour le {self.page}"


class Testimonial(BaseTimeStampModel):
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
    formatted_image = ImageSpecField(
        source='image',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(92, 91)
        ],
        format='JPEG',
        options={'quality': 90}
    )
    activate_at = models.BooleanField(
        default=False,
        verbose_name='actif',
        help_text='rendre visible cet témoignage ?'
    )

    objects = PageModelManager()

    class Meta:
        db_table = 'testimonial_db'
        ordering = ['-created_at', ]
        get_latest_by = ['-created_at', ]
        verbose_name_plural = 'Témoignages'
        indexes = [models.Index(fields=['id'],)]

    def __str__(self) -> str:
        return self.full_name

    def get_image_url(self):
        if self.formatted_image:
            return self.formatted_image.url
        return "https://via.placeholder.com/92x91"


class Campaign(BaseTimeStampModel, ModelSlugMixin):

    DESTOCKAGE = "Destockage"
    VENTE_FLASH = "Vente Flash"
    NOUVELLE_ARRIVAGE = "Nouvel Arrivage"

    OPTION_PROMOTION_CHOICES = (
        (DESTOCKAGE, 'Destockage'),
        (VENTE_FLASH, 'Vente Flash'),
        (NOUVELLE_ARRIVAGE, 'Nouvel Arrivage')
    )
    parent = models.CharField(
        max_length=120,
        verbose_name='titre de la campagne',
        **NULL_AND_BLANK
    )
    name = models.CharField(
        max_length=120,
        default=VENTE_FLASH,
        verbose_name='campagne',
        choices=OPTION_PROMOTION_CHOICES,
        **NULL_AND_BLANK
    )
    discount = models.IntegerField(
        verbose_name="pourcentage de réduction",
        validators=validators,
        **NULL_AND_BLANK
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=upload_campign_image_path,
    )
    formatted_image = ImageSpecField(
        source='image',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(1170, 399)
        ],
        format='JPEG',
        options={'quality': 90}
    )

    objects = PageModelManager()

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'Campagnes'
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return f"{self.name} (-{self.discount}%)"

    def get_image_url(self):
        if self.formatted_image:
            return self.formatted_image.url
        return "https://via.placeholder.com/680x380"

    @admin.display(description="cover")
    def show_image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.get_image_url()}" height="50"/>')
        return "https://via.placeholder.com/50x50"

    def get_campaigns(self):
        campaign = Promotion.objects.filter(campaign=self)
        return campaign

    @admin.display(description="total promos")
    def get_campaigns_count(self):
        return self.get_campaigns().count()

    @admin.display(description="% de réduction")
    def get_vouchers(self) -> str:
        if self.discount:
            return f"{self.discount}%"
        return "00"

    def get_absolute_url(self):
        return reverse(
            'promotion:promotion_detail',
            kwargs={'slug': str(self.slug)}
        )


class Promotion(ModelSlugMixin, ApplyDiscountModel, BaseTimeStampModel):

    campaign = models.ForeignKey(
        to="pages.Campaign",
        on_delete=models.PROTECT,
        verbose_name='campagne',
        related_name="campaigns"
    )

    class Meta:
        db_table = 'promotion_db'
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'promotions'
        indexes = [models.Index(fields=['id'],)]

    def _get_unique_slug(self):
        slug = slugify(self.campaign.name)
        unique_slug = slug
        num = 1
        while Promotion.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.campaign.name

    @property
    def discount(self):
        return self.campaign.discount

    def get_image_url(self):
        if self.campaign.formatted_image:
            return self.campaign.formatted_image.url
        return "https://via.placeholder.com/680x380"

    @admin.display(description="prix réduit")
    def get_price(self):
        single_product_price = [
            ((obj.price * self.campaign.discount)/100) for obj in self.get_products()
        ]
        return single_product_price

    def get_absolute_url(self):
        return reverse(
            'promotion:promotion_detail',
            kwargs={'slug': str(self.slug)}
        )

    def get_update_promo_url(self):
        return reverse(
            'dashboard_seller:promotion_update',
            kwargs={'slug': str(self.slug)}
        )

    def get_delete_promo_url(self):
        return reverse(
            'dashboard_seller:promotion_delete',
            kwargs={'slug': str(self.slug)}
        )


class Pub(ModelSlugMixin, BaseTimeStampModel):

    name = models.CharField(
        max_length=225,
        verbose_name="Titre",
        help_text="Saisir le titre de la publicité",
        **NULL_AND_BLANK
    )
    video = models.FileField(
        upload_to='videos/',
        validators=validate_video
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="actif/inactif ?"
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'Pubs Vidéos'
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return str(self.name.title())

    def get_video_url(self):
        return self.video.url


class Annonce(BaseTimeStampModel):

    name = models.CharField(
        max_length=225,
        verbose_name="Titre",
        help_text="Saisir le titre de la publicité",
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=upload_campign_image_path,
    )
    formatted_image = ImageSpecField(
        source='image',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(530, 285)
        ],
        format='JPEG',
        options={'quality': 90}
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="actif/inactif ?"
    )

    class Meta:
        db_table = 'annonce_db'
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'Annonces'
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return self.name

    def get_image_url(self):
        return self.image.url

    @admin.display(description="cover")
    def show_image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.get_image_url()}" height="50"/>')
        return "https://via.placeholder.com/50x50"


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
        editable=False,
        default=timezone.now
    )

    def __str__(self):
        return f"{self.full_name}: {self.email} - {self.phone}"

    @admin.display(description="date d'ajout")
    def date(self):
        return self.timestamp.date()

    class Meta:
        db_table = 'contact_db'
        ordering = ['-timestamp',]
        get_latest_by = ['-timestamp', ]
        verbose_name_plural = 'messages'
        indexes = [models.Index(fields=['id'])]


@receiver([models.signals.pre_save], sender=Pub)
@receiver([models.signals.pre_save], sender=Campaign)
def promotion_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=Campaign)
@receiver([models.signals.pre_save], sender=Annonce)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_image = Klass.objects.get(pk=instance.pk).image
            if old_image and old_image.url != instance.image.url:
                old_image.delete(save=False)
        except:
            pass
