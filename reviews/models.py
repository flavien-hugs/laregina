# reviews.models.py

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from catalogue.models import Product

from caching.caching import cache_update, cache_evict
from reviews.managers import ActiveProductReviewManager

User = settings.AUTH_USER_MODEL


class ProductReview(models.Model):
    """
    classe de modèle contenant des données
    de révision de produit associées à une instance de produit
    """
    
    RATINGS = ((1,1), (2,2), (3,3), (4,4), (5,5),)

    user = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.SET_NULL, 
        null=True
    )

    product = models.ForeignKey(
        Product,
        models.SET_NULL,
        null=True,
        verbose_name='produit'
    )
    email = models.EmailField(verbose_name='email')
    rating = models.PositiveSmallIntegerField(
        verbose_name='note',
        default=1,
        choices=RATINGS
    )
    content = models.TextField(verbose_name='avis client')
    created_time_at = models.DateField(auto_now_add=timezone.now())
    created_hour_at = models.TimeField(auto_now_add=timezone.now())
    is_approved = models.BooleanField(verbose_name='approuvé ?', default=False)

    objects = models.Manager()
    approved = ActiveProductReviewManager()

    class Meta:
        db_table = 'reviews_db'
        get_latest_by = ['-created_time_at', '-created_time_at', '-rating']
        ordering = ['-rating', '-created_time_at', '-created_time_at']
        verbose_name_plural = 'Avis des clients'

    def __str__(self):
        return f'{self.product.name}: {self.rating} - {self.created_time_at}'

    def get_absolute_url(self):
        return reverse('reviews:add_product_review', kwargs={'slug': self.product.slug})

    @property
    def cache_key(self):
        return self.get_absolute_url()

# attacher des signaux aux classes de modèles de review
# pour mettre à jour les données du cache sur les opérations
# de sauvegarde et de suppression
models.signals.post_save.connect(cache_update, sender=ProductReview)
models.signals.post_delete.connect(cache_evict, sender=ProductReview) 
