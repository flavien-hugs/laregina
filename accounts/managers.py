# accounts.managers.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_seller, **extra_fields):

        if not email:
            raise ValueError("Les utilisateurs doivent disposer d'une adresse électronique.")

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_seller=is_seller,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, False, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le super-utilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le super-utilisateur doit avoir is_superuser=True.")

        return self._create_user(email, password, False, **extra_fields)
