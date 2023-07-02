# reviews.models.py

from django.db import models
from django.urls import reverse

from catalogue.models import Product
from caching.caching import cache_update, cache_evict
from reviews.managers import ActiveProductReviewManager


class ProductReview(models.Model):

    RATINGS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    name = models.CharField(max_length=180, verbose_name="nom & prénoms", null=True)

    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, verbose_name="produit"
    )
    email = models.EmailField(verbose_name="email")
    rating = models.PositiveSmallIntegerField(
        verbose_name="note", default=1, choices=RATINGS
    )
    content = models.TextField(verbose_name="avis client")
    created_time_at = models.DateField(editable=False, auto_now_add=True)
    created_hour_at = models.TimeField(editable=False, auto_now_add=True)
    is_approved = models.BooleanField(verbose_name="approuvé ?", default=False)

    objects = models.Manager()
    approved = ActiveProductReviewManager()

    class Meta:
        ordering = ["-rating", "-created_time_at", "-created_time_at"]
        get_latest_by = ["-created_time_at", "-created_time_at", "-rating"]
        verbose_name_plural = "feedbacks"
        indexes = [
            models.Index(
                fields=["id"],
            ),
        ]

    def __str__(self):
        return f"{self.name} a donné son avis sur {self.product.name}: {self.rating} le {self.created_time_at}"

    def get_absolute_url(self):
        return reverse(
            "reviews:add_product_review", kwargs={"slug": str(self.product.slug)}
        )

    @property
    def cache_key(self):
        return self.get_absolute_url()


models.signals.post_save.connect(cache_update, sender=ProductReview)
models.signals.post_delete.connect(cache_evict, sender=ProductReview)
