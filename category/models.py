import logging

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from mptt.models import MPTTModel, TreeForeignKey

from helpers.utils import upload_promotion_image_path, unique_slug_generator
from helpers.models import ModelSlugMixin, BaseTimeStampModel


logger = logging.getLogger(__name__)
NULL_AND_BLANK = {"null": True, "blank": True}


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(MPTTModel, ModelSlugMixin, BaseTimeStampModel):
    parent = TreeForeignKey(
        to="self",
        db_index=True,
        related_name="children",
        on_delete=models.SET_NULL,
        verbose_name="catégorie principale",
        **NULL_AND_BLANK
    )
    name = models.CharField(
        max_length=120,
        db_index=True,
        verbose_name="sous-catégorie",
        help_text="Définir le nom de cette catégorie.",
    )
    image = models.ImageField(
        verbose_name="image",
        upload_to=upload_promotion_image_path,
        help_text="Ajouter une image à cette catégorie.",
        **NULL_AND_BLANK
    )
    formatted_image = ImageSpecField(
        source="image",
        processors=[ResizeToFill(1170, 399)],
        format="JPEG",
        options={"quality": 90},
    )
    is_active = models.BooleanField(verbose_name="active", default=True)

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        db_table = "category_db"
        verbose_name_plural = "catégories"
        unique_together = (
            "parent",
            "slug",
        )
        indexes = [models.Index(fields=["id"])]

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(ascending=True, include_self=True)
        except Exception:
            ancestors = []
        else:
            ancestors = [item.slug for item in ancestors]
        slug = []

        for item in range(len(ancestors)):
            slug.append("/".join(ancestors[: item + 1]))
        return slug

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            if k.name:
                full_path.append(k.name)
            k = k.parent
        return self.name

    @admin.display(description="catégorie")
    def categorie_name(self):
        return self.name.lower()

    def get_image_url(self):
        if self.image:
            return self.formatted_image.url
        return "static/img/categories/1.jpg"

    def get_products(self):
        from catalogue.models import Product

        products = Product.objects.filter(
            category__in=self.get_descendants(include_self=False)
        )
        return products

    @admin.display(description="nombre de produits")
    def products_count(self):
        return self.get_products().count()

    def promotions_category(self):
        from pages.models import Promotion

        products = self.get_products()
        promotions = Promotion.objects.filter(products__in=products)
        return (promotions).distinct()

    def get_absolute_url(self):
        return reverse("category:category_detail", kwargs={"slug": str(self.slug)})

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
        except Klass.DoesNotExist:
            logger.error("The Klass does not exist with that ID")
