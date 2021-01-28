# analytics.models.py

from django.db import models
from django.contrib.auth import get_user_model

from catalogue.models import Product

# User Manager
User = get_user_model()


class ObjectViewed(models.Model):
    """
        classe modèle pour suivre les pages vues par un client
    """

    class Meta:
        abstract = True
        verbose_name_plural = 'statistique'

    user = models.ForeignKey(User, models.SET_NULL, null=True, verbose_name='user')
    ip_address = models.CharField(verbose_name='adresse ip', max_length=225)
    tracking_id = models.CharField(max_length=50, default='', db_index=True)
    date_viewed_at = models.DateField(verbose_name='date de visite', auto_now=True)
    time_viewed_at = models.TimeField(verbose_name='date de visite', auto_now=True)


class ProductView(ObjectViewed):

    """
    suit les pages de produits que les clients consultent
    """

    product = models.ForeignKey(Product, models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user}: {self.product}'
