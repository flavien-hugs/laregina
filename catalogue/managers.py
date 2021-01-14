# catalogue.managers.py

from django.db import models
from django.db.models import Q
from django.utils import timezone


# STRUCTURE PRODUCT MODEL QUERYSET
class CataloqueQuerySet(models.query.QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(created_at__lte=now, is_active=True, is_stock=True)

    def search(self, query):
        lookups = (
            Q(name__icontains=query) | Q(category__name__icontains=query)
            | Q(description__icontains=query) | Q(slug__icontains=query)
            | Q(keywords__icontains=query) | Q(price__icontains=query)
        )
        return self.filter(lookups).distinct()


# STRUCTURE PRODUCT MODEL MANAGER
class CatalogueManager(models.Manager):

    def get_queryset(self):
        return CataloqueQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().active().search(query)

    def get_related(self, instance):
        product = self.get_queryset().filter(category=instance.category)
        qs = (product).exclude(id=instance.id).distinct()
        return qs
