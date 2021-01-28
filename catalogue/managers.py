# catalogue.managers.py

from django.db import models
from django.db.models import Q
from django.utils import timezone


# STRUCTURE PRODUCT MODEL QUERYSET
class CatalogueQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_stock=True)

    def product_recent_add(self):
        return self.filter(created_at__lte=timezone.now()).active()

    def search(self, query):
        lookups = (
            Q(name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(user__store__icontains=query)
            | Q(description__icontains=query)
            | Q(slug__icontains=query)
            | Q(keywords__icontains=query)
            | Q(price__icontains=query)
        )
        return self.filter(lookups).distinct()


# STRUCTURE PRODUCT MODEL MANAGER
class CatalogueManager(models.Manager):

    def get_queryset(self):
        return CatalogueQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def product_recent(self, *args, **kwargs):
        return self.get_queryset().product_recent_add()

    def search(self):
        return self.get_queryset().product_recent_add().search(query)

    def get_related(self, instance):
        product = self.get_queryset().filter(category=instance.category)
        return (product).exclude(id=instance.id).distinct()
