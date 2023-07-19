# checkout.managers.py
from django.db import models
from django.db.models import Q


class OrderManagerQuerySet(models.query.QuerySet):
    def trackink_order(self, query):
        lookups = Q(transaction_id__iexact=query)
        return self.filter(lookups)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def track_order(self, query):
        return self.get_queryset().trackink_order(query)
