# pages.managers.py

from django.db import models
from django.utils.timezone import now


class PageQuerySetMixin(models.QuerySet):
    def active(self):
        return self.filter(created_at__lte=now())

    def flash(self):
        from pages.models import Campaign

        return self.active().filter(name=Campaign.VENTE_FLASH).all()

    def destockage(self):
        from pages.models import Campaign

        return self.active().filter(name=Campaign.DESTOCKAGE).all()

    def arrivage(self):
        from pages.models import Campaign

        return self.active().filter(name=Campaign.NOUVELLE_ARRIVAGE).all()


class PageModelManager(models.Manager):
    def get_queryset(self):
        return PageQuerySetMixin(self.model, using=self._db)

    def published(self):
        return self.get_queryset().active()

    def ventes_flash(self):
        return self.get_queryset().flash()

    def destockages(self):
        return self.get_queryset().destockage()

    def nouvelle_arrivages(self):
        return self.get_queryset().arrivage()
