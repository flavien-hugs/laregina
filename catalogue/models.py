# catalogue.models.py

import random
from django.db import models
from django.conf import settings
from PIL import Image as PILImage
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from tagulous.models import TagField
from category.models import Category

from mptt.models import TreeManyToManyField
from core.utils import upload_image_path, unique_slug_generator

# User Manager
User = settings.AUTH_USER_MODEL


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0.00, 'blank': True, 'max_digits': 50, 'decimal_places': 00}


class Product(models.Model):
    user = models.ForeignKey(User, verbose_name='vendeur', on_delete=models.CASCADE)
    category = TreeManyToManyField(Category, verbose_name='catégorie', help_text="Selectionner la/les catégorie(s) du produit.")
    name = models.CharField(verbose_name='nom du produit', max_length=250)
    price = models.FloatField(verbose_name='prix de vente du produit', default=0.00)
    quantity = models.IntegerField(verbose_name='quantité de produit', default=1)
    description = models.TextField(verbose_name='description du produit', help_text="Définir votre produit.")
    image = models.ImageField(verbose_name='image descriptif', upload_to=upload_image_path)

    is_promotion = models.BooleanField("mettre le produit en promotion", default=False)
    promotion_price = models.DecimalField("prix de la promotion", **DECIMAFIELD_OPTION)

    # date de création et date de modification
    created_at = models.DateTimeField("date de création", auto_now_add=True, help_text="date d'ajout automatique du produit.")
    updated_at = models.DateTimeField('date de mise à jour', auto_now=True, help_text="date de mise à jour automatique du produit.")
    
    # mots clés
    keywords = TagField(verbose_name='mots clés', blank=True, help_text='Définir quelques mots clés.')
    # prix de la livraison
    
    is_external = models.BooleanField('Livrez-vous en dehors de votre pays ?', default=False)
    external_delivery = models.DecimalField('Prix de la livraison internationale', **DECIMAFIELD_OPTION)
    
    # pour plateforme d'achat uniquement
    is_active = models.BooleanField('produit disponible ?', default=True, help_text="ce produit est-il disponible ?")
    is_stock = models.BooleanField("en stock", default=True, help_text="produit en stock")
    slug = models.SlugField("URL du produit", blank=True, help_text="lien du prouit. Il est auto-générer, mais vous pouvez le modifier.")

    class Meta:
        ordering = ('-id',)
        get_latest_by = ['-created_at', 'updated_at']
        unique_together = ['name', 'slug']
        unique_together = ['name', 'slug']
        verbose_name = 'produit'
        verbose_name_plural = 'produit'

    def __str__(self):
        return self.name

    def get_image_url(self):
        """
            Return link to the first page small picture
        """
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img

    def show_image_tag(self):
        """
            Method to create a fake table field in read only mode
        """
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


@receiver(models.signals.pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='image produit')
    image = models.ImageField(verbose_name='image du produit', upload_to=upload_image_path, **NULL_AND_BLANK)

    class Meta:
        ordering = ('product',)
        verbose_name = 'image du produit'
        verbose_name_plural = 'images du produit'

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super(ProductImage, self).save()

        if self.image:
            t = PILImage.open(settings.MEDIA_ROOT + str(self.image)).convert("RGB")
            w = float(t.size[0])
            h = float(t.size[1])
            d = w/h
            h = int(640/d)
            t = t.resize((640, h), PILImage.ANTIALIAS)
            ts = t.resize((64, h/10), PILImage.ANTIALIAS)
            new_path = ''+str(self.image).split('/',3)[2]
            self.image = new_path
            t.save(settings.MEDIA_ROOT + str(self.image), 'JPEG')
            ts.save(settings.MEDIA_ROOT+new_path, 'JPEG')

        super(ProductImage, self).save()

@receiver(models.signals.pre_save, sender=ProductImage)
def delete_file(sender, instance, **kwargs):
    if not instance.product.slug:
        instance.product.slug = unique_slug_generator(instance)
