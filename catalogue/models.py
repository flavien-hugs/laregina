# catalogue.models.py

import random
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from tagulous.models import TagField
from category.models import Category
from catalogue.managers import CatalogueManager

from mptt.models import TreeManyToManyField
from core.utils import upload_image_path, unique_slug_generator

# User Manager
User = get_user_model()

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'blank': True, 'max_digits': 50, 'decimal_places': 2}


class Product(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        related_name='seller',
        verbose_name='vendeur'
    )
    category = TreeManyToManyField(Category, verbose_name='catégorie', help_text="Selectionner la/les catégorie(s) du produit.")
    name = models.CharField(verbose_name='nom du produit', max_length=250)
    price = models.DecimalField(verbose_name='prix', **DECIMAFIELD_OPTION)
    quantity = models.PositiveIntegerField(verbose_name='quantité', default=1, blank=True)
    old_price = models.DecimalField(verbose_name='ancien tarif', null=True, **DECIMAFIELD_OPTION)
    description = models.TextField(verbose_name='description du produit', help_text="Définir votre produit.")
    image = models.ImageField(verbose_name='image descriptif', upload_to=upload_image_path)

    is_promotion = models.BooleanField("mettre le produit en promotion", default=False)
    promotion_price = models.DecimalField("prix de la promotion", **DECIMAFIELD_OPTION)
    
    # mots clés
    keywords = TagField(
        verbose_name='mots clés',
        blank=True,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag'
    )

    is_external = models.BooleanField('Livrez-vous en dehors de votre pays ?', default=False)
    external_delivery = models.DecimalField('Prix de la livraison internationale', **DECIMAFIELD_OPTION)
    
    # pour plateforme d'achat uniquement
    is_active = models.BooleanField('produit disponible ?', default=True, help_text="ce produit est-il disponible ?")
    is_stock = models.BooleanField("en stock", default=True, help_text="produit en stock")
    slug = models.SlugField(
        verbose_name="URL du produit",
        blank=True,
        help_text='Unique value for product page URL, created automatically from name.'
    )

    # date de création et date de modification
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField("date de création", auto_now_add=True, help_text="date d'ajout automatique du produit.")
    updated_at = models.DateTimeField('date de mise à jour', auto_now_add=True, help_text="date de mise à jour automatique du produit.")

    objects = CatalogueManager()

    class Meta:
        ordering = ['-created_at', '-updated_at', '-timestamp']
        get_latest_by = ['-created_at', '-updated_at', '-timestamp']
        unique_together = ['user', 'name', 'slug']
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return self.name

    def get_sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def get_image_url(self):
        """Return link to the first page small picture"""
        try:
            images = self.productimage_set.first()
        except:
            return None
        
        if img:
            return img.image.url
        return img

    def show_image_tag(self):
        """Method to create a fake table field in read only mode"""
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.get_image_url()))
        else:
            return ""
    show_image_tag.allow_tags = True

    def show_description(self):
        return self.description
    show_description.allow_tags = True

    def recomended_products(self):
        products = Product.objects.filter(user=self.user, is_active=True).exclude(id=self.id)
        a = list(products)
        random.shuffle(a)
        return a[:5]

    # def get_absolute_url(self):
    #     return ('catalog_product', (), { 'product_slug': self.slug })

    # @property
    # def cache_key(self):
    #     return self.get_absolute_url()


@receiver(models.signals.pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance.name)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='image produit')
    image = models.ImageField(verbose_name='image du produit', upload_to=upload_image_path, **NULL_AND_BLANK)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('product',)
        verbose_name = 'image du produit'
        verbose_name_plural = 'images du produit'

    def __str__(self):
        return self.product.name

@receiver(models.signals.pre_save, sender=ProductImage)
def delete_file(sender, instance, **kwargs):
    if not instance.product.name:
        instance.product.name = unique_slug_generator(instance.name)
