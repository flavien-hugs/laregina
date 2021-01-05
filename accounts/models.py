# accounts/models.py

from django.db import models
from django.conf import settings

import cloudinary
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from django_extensions.db.fields import RandomCharField
from phonenumber_field.modelfields import PhoneNumberField

NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}


# Genère des URL aléatoires des profils, des messages et autres.
class RandomSlugModel(models.Model):
    slug = RandomCharField(length=10, lowercase=True, unique=True)

    class Meta:
        abstract = True


class UserProfile(RandomSlugModel):
    """
    Il s'agit d'une extension du modèle d'utilisateur par défaut,
    créé lors de l'enregistrement pour chaque utilisateur.
    Toutes les relations avec un utilisateur passent par ce modèle
    afin de maintenir la séparation avec le backend d'authentification.
    """

    ACCOUNT_TYPE_CHOICES = (
        ('0', "Je suis un acheteur"),
        ('1', "Je suis un vendeur"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', **UNIQUE_AND_DB_INDEX)
    type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES, default='0')
    name = models.CharField('boutique', max_length=200, **UNIQUE_AND_DB_INDEX)

    @property
    def is_seller(self):
        return self.type == self.ACCOUNT_TYPE_CHOICES[1][0]

    def __str__(self):
        return self.name


# Le SocialProfile est un modèle utilisé par les vendeurs pour se détailler
# et/ou fournir des informations complémentaires sur leurs services.
class StoreProfile(RandomSlugModel):
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='social')
    avatar = CloudinaryField('avatar', resource_type="avatar", transformation={"quality": "auto:eco"}, blank=True)
    tagline = models.CharField(max_length=150, **NULL_AND_BLANK)
    phone_number = PhoneNumberField('numéro de téléphone', **NULL_AND_BLANK)
    country = CountryField(blank_label='choisir le pays', **NULL_AND_BLANK)
    store_description = models.TextField('description de la boutique', max_length=2000, **NULL_AND_BLANK)

    def __str__(self):
        return self.owner.name

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'slug': self.slug})
