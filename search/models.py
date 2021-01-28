# search.models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchTerm(models.Model):

    """ stocke le texte de chaque recherche interne soumise """
    
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        verbose_name='user'
    )
    q = models.CharField(verbose_name='mot recherché', max_length=50)
    ip_address = models.CharField(verbose_name='ip adresse', max_length=225)
    tracking_id = models.CharField(verbose_name='tracking id', max_length=50, default='')
    date_search_at = models.DateField(verbose_name='date de recherche', auto_now_add=True)
    time_search_at = models.TimeField(verbose_name='heure de la recherche', auto_now=True)

    class Meta:
        db_table = 'search_db'
        ordering = ['-date_search_at', '-time_search_at']
        verbose_name_plural = 'recherche'

    def __str__(self):
        return str(self.q)