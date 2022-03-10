# category.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from mptt.models import MPTTModel, TreeForeignKey

from helpers.models import BaseTimeStampModel, ModelSlugMixin
from helpers.utils import upload_promotion_image_path, unique_slug_generator


NULL_AND_BLANK = {'null': True, 'blank': True}

class ActiveCategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(MPTTModel, ModelSlugMixin, BaseTimeStampModel):
    parent = TreeForeignKey(
        to='self',
        db_index=True,
        related_name='children',
        on_delete=models.SET_NULL,
        verbose_name='catégorie principale',
        **NULL_AND_BLANK
    )
    name = models.CharField(
        max_length=120, db_index=True,
        verbose_name='sous-catégorie',
        help_text="Définir le nom de cette catégorie.",
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to=upload_promotion_image_path,
        help_text="Ajouter une image à cette catégorie.",
        **NULL_AND_BLANK
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
    is_active = models.BooleanField(verbose_name='active', default=True)

    active = ActiveCategoryManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'category_db'
        verbose_name_plural = 'catégories'
        unique_together = (('parent', 'slug',))

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(ascending=True, include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slug = []

        for i in range(len(ancestors)):
            slug.append('/'.join(ancestors[:i+1]))
        return slug

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])

    @admin.display(description="catégorie")
    def categorie_name(self):
        return self.name.lower()

    def get_image_url(self):
        if self.image:
            return self.formatted_image.url
        return "static/img/categories/1.jpg"

    def get_products_in_category(self):
        from catalogue.models import Product
        products = Product.objects.filter(category=self)
        return products

    @admin.display(description="nombre de produits")
    def products_count(self):
        return len(self.get_products_in_category())

    def get_absolute_url(self):
        return reverse('category:category_detail', kwargs={'slug': str(self.slug)})

    @property
    def cache_key(self):
        return self.get_absolute_url()


@receiver([models.signals.pre_save], sender=Category)
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=Category)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_image = Klass.objects.get(pk=instance.pk).image
            if old_image and old_image.url != instance.image.url:
                old_image.delete(save=False)
        except:
            pass
