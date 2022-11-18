# catalogue.models.py

import logging
from itertools import chain

from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe

from catalogue.managers import CatalogueManager
from caching.caching import cache_update, cache_evict

from mptt.models import TreeForeignKey
from helpers.utils import upload_image_path, unique_slug_generator
from helpers.models import BaseTimeStampModel

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

logger = logging.getLogger(__name__)
NULL_AND_BLANK = {"null": True, "blank": True}
DECIMAFIELD_OPTION = {"max_digits": 50, "decimal_places": 0}
UNIQUE_AND_DB_INDEX = {"null": False, "unique": True, "db_index": True}


class Product(BaseTimeStampModel):
    user = models.ForeignKey(
        to="accounts.User",
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_seller": True,
        },
        verbose_name="vendeur",
        help_text="magasin en charge de la vente.",
    )
    category = TreeForeignKey(
        to="category.Category",
        on_delete=models.PROTECT,
        verbose_name="catégorie",
        help_text="Selectionner la catégorie du produit.",
    )
    name = models.CharField(
        verbose_name="nom du produit", max_length=255, help_text="Le nom du produit"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="quantité", default=1, help_text="quantité de produit"
    )
    price = models.DecimalField(
        default=0,
        verbose_name="prix de vente",
        help_text="Le prix du produit",
        **DECIMAFIELD_OPTION,
    )
    description = models.TextField(
        verbose_name="description du produit", help_text="Définir votre produit."
    )
    keywords = models.CharField(
        verbose_name="mots clés",
        blank=True,
        max_length=50,
        help_text="Comma-delimited set of SEO keywords for keywords meta tag",
    )
    is_external = models.BooleanField(
        default=False,
        verbose_name="Ce produit peut-être livrer en dehors de votre pays ?",
        help_text="Ce produit peut-être livrer en dehors de votre pays ?",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="produit disponible ?",
        help_text="ce produit est-il disponible ?",
    )
    slug = models.SlugField(
        verbose_name="URL du produit",
        blank=True,
        unique=True,
        help_text="Unique value for product page URL, created automatically from name.",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CatalogueManager()

    class Meta:
        db_table = "catalogue_db"
        unique_together = ["slug"]
        index_together = (("slug",),)
        ordering = ["-created_at", "-updated_at", "-timestamp"]
        get_latest_by = ["-created_at", "-updated_at", "-timestamp"]
        verbose_name_plural = "produits"
        indexes = [models.Index(fields=["id"], name="id_index_product")]

    def __str__(self):
        return self.name

    def attributes(self):
        values = ProductAttributeValue.objects.filter(product=self)
        return values

    def get_price(self):
        for obj in self.get_vouchers_price():
            return obj

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))

    def product_price(self):
        if self.get_price() is not None and self.get_price() < self.price:
            new_price = self.price - self.get_price()
            return new_price
        return self.price

    @admin.display(description="prix du produit")
    def get_product_price(self):
        return self.product_price()

    def get_discount_products(self):
        from voucher.models import Voucher
        from pages.models import Promotion

        products = Voucher.objects.prefetch_related("products").filter(products=self)
        promotions = Promotion.objects.prefetch_related("products").filter(
            products=self
        )
        objects_list = chain(promotions, products)

        return objects_list

    @admin.display(description="% de réduction", empty_value="00")
    def get_vouchers(self):
        for obj in self.get_discount_products():
            voucher = obj.discount
            return voucher

    @admin.display(description="prix réduit", empty_value="00")
    def get_vouchers_price(self):
        if self.get_discount_products():
            discount = [
                ((obj.discount * self.price) / 100)
                for obj in self.get_discount_products()
            ]
            return discount
        return None

    @admin.display(description="description du produit")
    def get_product_description(self):
        return self.description

    @admin.display(description="boutique du produit")
    def get_product_shop(self):
        return self.user.store

    @admin.display(description="contact de la boutique")
    def get_product_contact(self):
        return self.user.phone

    @admin.display(description="score du produit")
    def avaregereview(self):
        from reviews.models import ProductReview

        reviews = ProductReview.objects.filter(product=self).aggregate(
            avarage=Avg("rating")
        )
        avg = 0
        if reviews["avarage"] is not None:
            avg = "%.1f" % float(reviews["avarage"])
        return avg

    def percentaverage(self):
        percent = "%.0f" % (float(self.avaregereview()) * 10)
        return percent

    @admin.display(description="nombre de commentaire sur le produit")
    def countreview(self):
        from reviews.models import ProductReview

        reviews = ProductReview.objects.filter(product=self).aggregate(
            count=Count("id")
        )
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    @admin.display(description="liste des avis")
    def review_list(self):
        from reviews.models import ProductReview

        rvw_list = ProductReview.objects.prefetch_related("product").filter(
            product=self
        )
        return rvw_list

    def get_absolute_url(self):
        return reverse(
            "catalogue:product_detail",
            kwargs={"slug": str(self.slug), "pk": int(self.pk)},
        )

    def get_update_url(self):
        return reverse(
            "dashboard_seller:product_update", kwargs={"slug": str(self.slug)}
        )

    def get_delete_url(self):
        return reverse(
            "dashboard_seller:product_delete", kwargs={"slug": str(self.slug)}
        )

    def cache_key(self):
        return self.get_absolute_url()

    def images(self):
        return ProductImage.objects.filter(product=self)

    def get_image_url(self):
        if self.images():
            return str(self.images().first().formatted_image.url)
        return "https://via.placeholder.com/300x300"

    @admin.display(description="image du produit")
    def get_product_image(self):
        if self.images().first() is not None:
            return mark_safe(f"<img src='{self.get_image_url()}' height='50'/>")
        return "https://via.placeholder.com/50x50"

    def product_image_url(self):
        if self.images():
            return str(self.images().first().formatted_image.url)
        return "https://via.placeholder.com/300x300"

    def feebacks_products(self):
        from reviews.models import ProductReview

        return ProductReview.objects.filter(product=self)

    def promotions(self):
        from pages.models import Promotion

        promotion = Promotion.objects.prefetch_related("products").filter(
            product__in=self
        )
        return promotion


class ProductAttributeValue(models.Model):
    """
    Déclinaison de produit déterminée par
    des attributs comme la couleur, etc.
    """

    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XS = "XS"

    SIZE_CHOICES = (
        (XS, "XS"),
        (S, "S"),
        (M, "M"),
        (L, "L"),
        (XL, "XL"),
    )
    product = models.ForeignKey(
        to="catalogue.Product", on_delete=models.CASCADE, verbose_name="attribut"
    )
    size = models.CharField(
        max_length=2,
        default=M,
        verbose_name="tailles",
        choices=SIZE_CHOICES,
        help_text="Sélectionner une taille",
    )

    class Meta:
        verbose_name_plural = "Tailles"
        indexes = [models.Index(fields=["id"])]

    def __str__(self):
        return f"{self.product}, {self.size}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        to="catalogue.Product", on_delete=models.CASCADE, verbose_name="image produit"
    )
    image = models.ImageField(
        verbose_name="image du produit",
        upload_to=upload_image_path,
        help_text="Taille: 300x300px",
    )
    formatted_image = ImageSpecField(
        source="image",
        processors=[Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 90},
    )
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = "product_image_db"
        ordering = ["-updated", "-timestamp"]
        verbose_name_plural = "galleries du produit"

    def __str__(self):
        return self.product.name.lower()

    def get_image_url(self):
        if self.image:
            return self.formatted_image.url
        return "/static/img/default.jpeg"


@receiver([models.signals.pre_save], sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=ProductImage)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_image = Klass.objects.get(pk=instance.pk).image
            if old_image and old_image.url != instance.image.url:
                old_image.delete(save=False)
        except Klass.DoesNotExist:
            logger.error("The Klass does not exist with that ID")
