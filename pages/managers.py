# pages.managers.py

from django.db import models
from django.utils.timezone import now


class PageQuerySetMixin(models.QuerySet):

    def active(self):
        return self.filter(
            created_at__lte=tnow
        )

    def vente_flash(self):
        from pages.models import Campaign
        return self.active().filter(name=Campaign.VENTE_FLASH)

    def destockage(self):
        from pages.models import Campaign
        return self.active().filter(name=Campaign.DESTOCKAGE)

    def nouvelle_arrivage(self):
        from pages.models import Campaign
        return self.active().filter(name=Campaign.NOUVELLE_ARRIVAGE)


class PageModelManager(models.Manager):

    def get_queryset(self):
        return PageQuerySetMixin(self.model, using=self._db)

    def published(self):
        return self.get_queryset().active()

    def ventes_flash(self):
        return self.get_queryset().vente_flash()

    def destockages(self):
        return self.get_queryset().destockage()

    def nouvelle_arrivages(self):
        return self.get_queryset().nouvelle_arrivage()
