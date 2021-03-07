# catalogue.models.py

from PIL import Image
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe

from core import settings
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
        User,
        models.CASCADE,
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
        max_length=120,
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
        blank=True,
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
        verbose_name_plural = 'produit'

    def __str__(self):
        return self.name

    def __repr__(self):
       return self.__str__()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

    def get_product_image(self):
        """
        Méthode pour créer un champ de table en
        mode lecture seule
        """
        if self.productimage_set.first() is not None:
            return mark_safe('<img src="{url}" height="50"/>'.format(url=self.get_image_url()))
        else:
            return ""
    get_product_image.short_description = 'image'

    def get_product_description(self):
        return self.description
    get_product_description.short_description = 'description'

    def get_product_shop(self):
        return self.user.store
    get_product_shop.short_description = 'magasin'

    # calcul de la moyenne des note de commentaire
    def avaregereview(self):
        from reviews.models import ProductReview
        reviews = ProductReview.objects.filter(product=self).aggregate(avarage=Avg('rating'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = "%.1f" % float(reviews["avarage"])
        return avg

    # compter le nombre de commentaires
    def countreview(self):
        from reviews.models import ProductReview
        reviews = ProductReview.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

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

        """
        obtient d'autres instances de produit
        qui ont été combinées avec l'instance
        actuelle dans des commandes antérieures et 
        inclut les commandes qui ont été passées
        par des utilisateurs anonymes qui ne se
        sont pas enregistrés
        """

        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=order_items).distinct()
        return object_list

    
    def cross_sells_user(self):

        """
        NOTE : les utilisateurs qui ont acheté
        ce produit ont également acheté....
        
        obtient d'autres instances de produits
        qui ont été commandées par d'autres clients
        enregistrés qui ont également commandé
        l'instance en cours. Utilise toutes les
        commandes passées de chaque client
        enregistré et pas seulement l'ordre dans
        lequel l'instance actuelle a été achetée
        """

        from checkout.models import Order, OrderItem
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=items).distinct()
        return object_list
    
    def cross_sells_hybrid(self):
        
        """
        obtient d'autres exemples de produits qui ont été combinés
        avec l'exemple actuel dans des commandes passées par des
        clients non enregistrés, et tous les produits qui ont déjà
        été commandés par des clients enregistrés
        """
        
        from checkout.models import Order, OrderItem
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(
            Q(order__in=orders) | Q(order__user__in=users)
            ).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=items).distinct()
        return object_list


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
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

    def __repr__(self):
       return self.__str__()


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
        instance.slug = unique_slug_generator(instance.name)
