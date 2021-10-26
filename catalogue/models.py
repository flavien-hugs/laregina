# catalogue.models.py

from PIL import Image
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe

from category.models import Category
from catalogue.managers import CatalogueManager
from caching.caching import cache_update, cache_evict

from mptt.models import TreeForeignKey
from core.utils import upload_image_path, unique_slug_generator

User = settings.AUTH_USER_MODEL

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'max_digits': 50, 'decimal_places': 0}


class Product(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_seller': True,},
        verbose_name='vendeur',
        help_text="magasin en charge de la vente."
    )
    category = TreeForeignKey(
        Category,
        models.CASCADE,
        verbose_name='catégorie',
        help_text="Selectionner la catégorie du produit."
    )
    name = models.CharField(
        verbose_name='nom du produit',
        max_length=255,
        help_text="Le nom du produit"
    )
    quantity = models.PositiveIntegerField(
        verbose_name='quantité',
        default=1,
        help_text="quantité de produit"
    )
    price = models.DecimalField(
        verbose_name='prix de vente',
        help_text="Le prix du produit",
        **DECIMAFIELD_OPTION,
    )
    description = models.TextField(
        verbose_name='description du produit',
        help_text="Définir votre produit."
    )
    keywords = models.CharField(
        verbose_name='mots clés',
        blank=True, max_length=50,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag'
    )
    is_external = models.BooleanField(
        verbose_name='Ce produit peut-être livrer en dehors de votre pays ?',
        default=False,
        help_text='Ce produit peut-être livrer en dehors de votre pays ?'
    )
    is_active = models.BooleanField(
        verbose_name='produit disponible ?',
        default=True,
        help_text="ce produit est-il disponible ?"
    )
    slug = models.SlugField(
        verbose_name="URL du produit",
        blank=True, unique=True,
        help_text='Unique value for product page URL, created automatically from name.'
    )
    created_at = models.DateTimeField(
        verbose_name="date de création",
        auto_now_add=True,
        help_text="date d'ajout automatique du produit"
    )
    updated_at = models.DateTimeField(
        verbose_name='date de mise à jour',
        auto_now_add=True,
        help_text="date de mise à jour automatique du produit."
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CatalogueManager()

    class Meta:
        db_table = 'catalogue_db'
        unique_together = ['slug']
        index_together = (('slug',),)
        ordering = ['-created_at', '-updated_at', '-timestamp']
        get_latest_by = ['-created_at', '-updated_at', '-timestamp']
        verbose_name_plural = 'produits'
        indexes = [models.Index(fields=['id'], name='id_index_product'),]

    def __str__(self):
        return self.name

    @admin.display(description="prix du produit")
    def get_product_price(self):
        return self.price

    def get_image_url(self):
        try:
            image = self.productimage_set.first()
        except:
            return ''
        
        if image:
            return image.image.url
        return image

    @admin.display(description="image du produit")
    def get_product_image(self):
        if self.productimage_set.first() is not None:
            return mark_safe('<img src="{url}" height="50"/>'.format(url=self.get_image_url()))
        else:
            return ""

    @admin.display(description="description du produit")
    def get_product_description(self):
        return self.description

    @admin.display(description="magasin du produit")
    def get_product_shop(self):
        return self.user.store

    @admin.display(description="score du produit")
    def avaregereview(self):
        from reviews.models import ProductReview
        reviews = ProductReview.objects.filter(product=self).aggregate(avarage=Avg('rating'))
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
        reviews = ProductReview.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    @admin.display(description="liste des avis")
    def review_list(self):
        from reviews.models import ProductReview
        rvw_list = ProductReview.objects.all().filter(product=self)
        return rvw_list

    def get_absolute_url(self):
        return reverse(
            'catalogue:product_detail', kwargs={'slug': str(self.slug)}
        )

    def get_update_url(self):
        return reverse(
            'seller:product_update', kwargs={'slug': str(self.slug)}
        )

    def get_delete_url(self):
        return reverse(
            'seller:product_delete', kwargs={'slug': str(self.slug)}
        )

    def cache_key(self):
        return self.get_absolute_url()

    def cross_sells(self):
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=order_items).distinct()
        return object_list

    def cross_sells_hybrid(self):
        from django.db.models import Q
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        items = OrderItem.objects.filter(Q(order__in=orders)).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=items).distinct()
        return object_list


class ProductImage(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='image produit'
    )
    image = models.ImageField(
        verbose_name='image du produit',
        upload_to=upload_image_path,
        help_text="Taille: 300x300px"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        auto_now=False
    )
    updated = models.DateTimeField(
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        db_table = 'product_image_db'
        ordering = ['-updated', '-timestamp']
        verbose_name_plural = 'images du produit'

    def __str__(self):
        return self.product.name

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
            if img.height > 300 and img.width > 300: 
                output_size = (300, 300) 
                img.thumbnail(output_size)
                img.convert('RGB') 
                img.save(self.image.path)


@receiver([models.signals.pre_save], sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
