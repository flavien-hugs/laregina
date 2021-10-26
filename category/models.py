# category.models.py

from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey
from core.utils import upload_image_path, unique_slug_generator


class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(MPTTModel):
    parent = TreeForeignKey(
        to='self',
        related_name='children',
        on_delete=models.SET_NULL,
        db_index=True, blank=True, null=True,
        verbose_name='catégorie principale',
    )
    name = models.CharField(
        max_length=120,
        db_index=True,
        verbose_name='sous-catégorie',
    )
    image = models.ImageField(
        verbose_name='cover catégorie',
        upload_to=upload_image_path,
        null=True, blank=True,
        help_text="Taille: 300x300px"
    )
    slug = models.SlugField(
        verbose_name='lien',
        db_index=True, unique=True,
        blank=True, null=True

    )
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
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
        return self.name

    def get_products_in_category(self):
        from catalogue.models import Product
        products = Product.objects.filter(category=self)
        return products

    def get_absolute_url(self):
        return reverse('category:category_detail', kwargs={'slug': str(self.slug)})

    @property
    def cache_key(self):
        return self.get_absolute_url()


@receiver([models.signals.pre_save], sender=Category)
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
