# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import UserManager
from core.utils import generate_key, upload_image_path


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'null': False, 'unique': True, 'db_index': True}

class Subject(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'sujet'
        verbose_name_plural = 'sujets'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    """ 
        Un modèle d'utilisateur complet avec des autorisations compatibles avec l'administrateur qui utilise 
        un champ de courrier électronique complet comme nom d'utilisateur. Email et mot de passe sont requis.
        Les autres champs sont facultatifs. 
    """

    GENDER_CHOICES = (('Mr', 'Mr'), ('Mme', 'Mme'), ('Mlle', 'Mlle'),)

    email = models.EmailField(verbose_name='email', max_length=254, unique=True,
        error_messages={'unique': "Un utilisateur disposant de ce courriel existe déjà.",})
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default="Mr")
    name = models.CharField(verbose_name="nom", max_length=120)
    store = models.CharField(verbose_name='boutique', max_length=254, **NULL_AND_BLANK)
    phone_number = PhoneNumberField('numéro de téléphone')
    whatsapp_number = PhoneNumberField('numéro de téléphone WhatsApp', null=True)
    country = CountryField(blank_label='choisir le pays', **NULL_AND_BLANK)
    city = models.CharField(verbose_name='ville', max_length=250, **NULL_AND_BLANK)
    address = models.CharField(verbose_name='adresse', max_length=250, **NULL_AND_BLANK)
    interests = models.ManyToManyField(Subject, related_name='interested_customers')
    store_description = models.TextField('description de la boutique', max_length=2000, **NULL_AND_BLANK)
    logo = models.ImageField(verbose_name='logo', upload_to=upload_image_path, **NULL_AND_BLANK)
    facebook = models.CharField(verbose_name='facebook', max_length=250, **NULL_AND_BLANK)
    twitter = models.CharField(verbose_name='twitter', max_length=250, **NULL_AND_BLANK)
    linkedin = models.CharField(verbose_name='linkedin', max_length=250, **NULL_AND_BLANK)
    instagramm = models.CharField(verbose_name='instagramm', max_length=250, **NULL_AND_BLANK)
    is_staff = models.BooleanField(verbose_name='statut équipe', default=False)
    is_superuser = models.BooleanField(verbose_name='administrateur', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_buyer = models.BooleanField(verbose_name='Acheteur', default=False)
    is_seller = models.BooleanField(verbose_name='Vendeur', default=False)
    last_login = models.DateTimeField(**NULL_AND_BLANK)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('-date_joined',)
        index_together = (('email',),)
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return self.email

    def get_fullname(self):
        if self.gender and self.name:
            fullname = '{gender} {name}'.format(gender=self.gender, name=self.name)
            return fullname.strip()
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have permissions to view the app `app_label` ?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label` ?"
        return True

    def get_absolute_url(self):
        return "/users/{}/".formal(self.email)
