# catalogue.managers.py

from django.db import models
from django.db.models import Q


# STRUCTURE PRODUCT MODEL QUERYSET
class CataloqueQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_stock=True)


# STRUCTURE PRODUCT MODEL MANAGER
class CatalogueManager(models.Manager):

    def get_queryset(self):
        return CataloqueQuerySet(self.model, using=self._db)

    def __getattr__(self, attr, *args):
        return getattr(self.get_queryset(), attr, *args)

    def get_related(self, instance):
        product = self.get_queryset().filter(categories=instance.categories)
        qs = (product).exclude(id=instance.id).distinct()
        return qs