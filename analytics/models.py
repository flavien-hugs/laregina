# analytics.models.py

from django.db import models

from core import settings
from catalogue.models import Product

# User Manager
User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    """
    class modèle pour suivre les pages vues par un client
    """

    user = models.ForeignKey(User, models.SET_NULL, null=True, verbose_name='user')
    ip_address = models.CharField(verbose_name='adresse ip', max_length=225)
    tracking_id = models.CharField(max_length=50, default='', db_index=True)
    date_viewed = models.DateField(verbose_name='date de visite', auto_now=True)
    time_viewed = models.TimeField(verbose_name='heure de visite', auto_now=True)

    class Meta:
        abstract = True
        db_table = 'analiytics_db'
        index_together = (('user',),)
        ordering = ('-date_viewed', '-time_viewed')
        get_latest_by = ('-date_viewed', '-time_viewed')
        verbose_name_plural = 'statistiques'


class ProductView(ObjectViewed):

    """
    suit les pages de produits que les clients consultent
    """

    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        verbose_name='produit',
        null=True
    )

    def __str__(self):
        return f'{self.user}: {self.product}'
