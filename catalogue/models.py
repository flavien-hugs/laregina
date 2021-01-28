# catalogue.models.py

import random
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import Avg, Count, Q
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from tagulous.models import TagField
from category.models import Category
from catalogue.managers import CatalogueManager
from caching.caching import cache_update, cache_evict

from mptt.models import TreeForeignKey
from core.utils import upload_image_path, unique_slug_generator

# User Manager
User = get_user_model()

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}
DECIMAFIELD_OPTION = {'default': 0, 'max_digits': 50, 'decimal_places': 0}


class Product(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        limit_choices_to={
            'is_staff': True,
            'is_seller': True,
            'is_superuser': True
        },
        related_name='seller',
        verbose_name='vendeur',
        help_text="Le magasin en charge de la vente."
    )
    category = TreeForeignKey(
        Category,
        models.CASCADE,
        verbose_name='catégorie',
        help_text="Selectionner la/les catégorie(s) du produit."
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
        verbose_name='prix',
        help_text="Le prix du produit",
        **DECIMAFIELD_OPTION,
    )
    old_price = models.DecimalField(
        verbose_name='ancien tarif',
        null=True,
        blank=True,
        **DECIMAFIELD_OPTION
    )
    description = models.TextField(
        verbose_name='description du produit',
        help_text="Définir votre produit."
    )
    is_promotion = models.BooleanField(
        verbose_name="mettre le produit en promotion",
        default=False
    )
    promotion_price = models.DecimalField(
        "prix de la promotion",
        blank=True,
        **DECIMAFIELD_OPTION
    )
    keywords = TagField(
        verbose_name='mots clés',
        blank=True,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag'
    )
    is_external = models.BooleanField(
        verbose_name='Livrez-vous en dehors de votre pays ?',
        default=False,
        help_text='Ce produit peut-être livrer en dehors de votre pays ?'
    )
    external_delivery = models.DecimalField(
        verbose_name='Prix de la livraison internationale',
        **DECIMAFIELD_OPTION
    )
    is_active = models.BooleanField(
        verbose_name='produit disponible ?',
        default=True,
        help_text="ce produit est-il disponible ?"
    )
    is_stock = models.BooleanField(
        verbose_name="en stock",
        default=True,
        help_text="produit en stock"
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
    nb_view = models.PositiveIntegerField(
        verbose_name='Nombre de vues du produit',
        default=0,
        blank=True
    )

    objects = CatalogueManager()

    class Meta:
        ordering = ['-created_at', '-updated_at', '-timestamp']
        get_latest_by = ['-created_at', '-updated_at', '-timestamp']
        unique_together = ['slug']
        verbose_name_plural = 'produits'

    def __str__(self):
        return self.name

    def __repr__(self):
       return self.__str__()

    @property
    def get_sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(instance.name)
        super().save(*args, **kwargs)

    def get_image_url(self):
        try:
            image = self.productimage_set.first()
        except:
            return None
        
        if image:
            return image.image.url
        return image

    @property
    def show_image_tag(self):
        """
        Méthode pour créer un champ de table en
        mode lecture seule
        """
        if self.productimage_set.first() is not None:
            return mark_safe('<img src="{url}" height="50"/>'.format(url=self.get_image_url()))
        else:
            return ""

    @property
    def show_description(self):
        return self.description

    @property
    def recomended_product(self):
        products = Product.objects.filter(
            user=self.user, is_active=True).exclude(id=self.id)
        a = list(products)
        random.shuffle(a)
        return a[:5]

    # get avarege review
    def avaregereview(self):
        from reviews.models import ProductReview
        reviews = ProductReview.objects.filter(
            product=self).aggregate(avarage=Avg('rating'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = "%.1f" % float(reviews["avarage"])
        return avg

    # count review
    def countreview(self):
        from reviews.models import ProductReview
        reviews = ProductReview.objects.filter(
            product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


    def get_absolute_url(self):
        return reverse('catalogue:product_detail', kwargs={'slug': str(self.slug)})

    @property
    def cache_key(self):
        return self.get_absolute_url()

    def cross_sells(self):

        """
        obtient d'autres instances de produit
        qui ont été combinées avec l'instance
        actuelle dans des commandes antérieures.
        inclut les commandes qui ont été passées
        par des utilisateurs anonymes qui ne se
        sont pas enregistrés
        """

        from order.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=order_items).distinct()
        print(object_list)
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

        from order.models import Order, OrderItem
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=items).distinct()
        print(products)
        return object_list
    
    def cross_sells_hybrid(self):
        
        """
        obtient d'autres exemples de produits qui ont été combinés
        avec l'exemple actuel dans des commandes passées par des
        clients non enregistrés, et tous les produits qui ont déjà
        été commandés par des clients enregistrés
        """
        
        from order.models import Order, OrderItem
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(
            Q(order__in=orders) | Q(order__user__in=users)
            ).exclude(product=self)
        object_list = Product.objects.filter(orderitem__in=items).distinct()
        print(object_list)
        return object_list


class Variation(models.Model):
    product = models.ForeignKey(
        Product,
        models.CASCADE,
        related_name='varition',
        verbose_name='variant du produit',
        help_text="variante du produit"
    )
    name = models.CharField(
        verbose_name='le nom du produit',
        max_length=120,
        help_text="variante du produit"
    )
    price = models.DecimalField(
        verbose_name='le prix du produit',
        help_text="le prix du produit",
        **DECIMAFIELD_OPTION
    )
    sale_price = models.DecimalField(
        verbose_name='le prix de vente du produit',
        help_text="le prix du produit",
        **DECIMAFIELD_OPTION
    )
    is_active = models.BooleanField(
        verbose_name='disponibilité du produit',
        default=True,
        help_text="décoché cette case si ce produit est indisponible."
    )
    inventory = models.PositiveIntegerField(
        verbose_name='inventaire du produit',
        help_text="ce produit est en stock ?",
        **NULL_AND_BLANK
    )

    def __str__(self):
        return self.name

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    @property
    def get_html_price(self):
        if self.sale_price is not None:
            html_text = "<span class='sale-price'>{sale_price}</span> <span class='og-price'>{price}</span>".format(
                sale_price=self.sale_price, price=self.price)
        else:
            html_text = "<span class='price'>{price}</span>".format(price=self.price)
        return mark_safe(html_text)

    @property
    def get_title(self):
        return "{vproduct} - {product} ".format(vproduct=self.product.name, product=self.name)

    def get_absolute_url(self):
        return self.product.get_absolute_url()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='image produit')
    image = models.ImageField(verbose_name='image du produit', upload_to=upload_image_path)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('product',)
        verbose_name = 'image du produit'
        verbose_name_plural = 'images du produit'

    def __str__(self):
        return self.product.name

    def __repr__(self):
       return self.__str__()

    """def save(self, *args, **kwargs): 
        super().save(*args, **kwargs) 
        img = Image.open(self.image.path) 
        if img.height > 400 or img.width > 400: 
            output_size = (300, 300) 
            img.thumbnail(output_size) 
            img.save(self.image.path)""" 


@receiver([models.signals.pre_save], sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance.name)


@receiver([models.signals.post_save], sender=Product)
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    pvariation = product.varition.all()
    if pvariation.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.name = "Default"
        new_var.price = product.price
        new_var.save()


@receiver([models.signals.post_delete], sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete()

# attacher des signaux aux classes de modèles de produit
# pour mettre à jour les données du cache sur les opérations
# de sauvegarde et de suppression
# models.signals.post_save.connect(cache_update, sender=Product)
# models.signals.post_delete.connect(cache_evict, sender=Product) 
