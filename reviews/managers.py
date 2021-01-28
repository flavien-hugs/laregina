# reviews.managers.py

from django.db import models
from django.db.models import Q
from django.utils import timezone


class ActiveProductReviewManager(models.Manager):
    
    """
    La classe Manager ne renvoie que les examens de
    produits dont chaque instance est approuvée.
    """

    def all(self):
        return super().filter(
            created_time_at__lte=timezone.now(),
            created_hour_at__lte=timezone.now(),
            is_approved=True
        )
