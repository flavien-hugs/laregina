from django.db import models


class ObjectViewed(models.Model):
    ip_address = models.CharField(verbose_name="adresse ip", max_length=225)
    tracking_id = models.CharField(max_length=50, default="", db_index=True)
    date_viewed = models.DateField(verbose_name="date de visite", auto_now=True)
    time_viewed = models.TimeField(verbose_name="heure de visite", auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-date_viewed", "-time_viewed")
        get_latest_by = ("-date_viewed", "-time_viewed")
        verbose_name_plural = "statistiques"


class ProductView(ObjectViewed):
    product = models.ForeignKey(
        to="catalogue.Product",
        on_delete=models.CASCADE,
        verbose_name="produit",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.product}"
