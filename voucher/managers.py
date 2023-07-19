from django.db import models


class VoucherQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class VoucherManager(models.Manager):
    def get_queryset(self):
        return VoucherQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()
