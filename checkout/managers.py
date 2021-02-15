# checkout.managers.py

from django.db import models
from django.utils import timezone


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-timestamp", "-modify_date")

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)

        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(modify_date__gte=start_date)
        return self.filter(modify_date__gte=start_date).filter(modify_date__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(modify_date__day__gte=now.day)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def recent_order(self, *args, **kwargs):
        return self.get_queryset().recent()
