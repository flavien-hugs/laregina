# search.models.py

from django.db import models

from core import settings

# user manager
User = settings.AUTH_USER_MODEL


class SearchTerm(models.Model):

    """
    stocke le texte de chaque recherche interne soumise
    """
    
    user = models.ForeignKey(
        to="accounts.User",
        on_delete=models.SET_NULL,
        verbose_name='user'
        null=True
    )
    q = models.CharField(
        verbose_name='mot recherché',
        max_length=50
    )
    ip_address = models.CharField(
        verbose_name='adresse IP',
        max_length=225,
    )
    date_search_at = models.DateField(
        verbose_name='date de recherche',
        auto_now_add=True
    )
    time_search_at = models.TimeField(
        verbose_name='heure de la recherche',
        auto_now=True
    )

    class Meta:
        db_table = 'search_db'
        ordering = ['-date_search_at', '-time_search_at']
        get_latest_by = ['-date_search_at', '-time_search_at']
        verbose_name_plural = 'recherches'
        indexes = [models.Index(fields=['id'],)]

    def __str__(self):
        return str(self.q)
