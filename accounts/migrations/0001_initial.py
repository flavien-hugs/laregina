# Generated by Django 3.1.5 on 2021-01-12 18:46

import core.utils
from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('store_id', models.CharField(blank=True, max_length=120, unique=True, verbose_name='ID STORE')),
                ('email', models.EmailField(error_messages={'unique': 'Un utilisateur disposant de ce courriel existe déjà.'}, max_length=254, unique=True, verbose_name='email')),
                ('civility', models.CharField(choices=[('Mr', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')], default='Mr', max_length=4, verbose_name='civilité')),
                ('name', models.CharField(max_length=120, verbose_name='nom & prénoms')),
                ('store', models.CharField(blank=True, max_length=254, null=True, verbose_name='boutique')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='numéro de téléphone')),
                ('whatsapp_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='numéro de téléphone WhatsApp')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True, verbose_name='ville')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='adresse')),
                ('store_description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='description de la boutique')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_image_path, verbose_name='logo')),
                ('facebook', models.URLField(blank=True, max_length=250, null=True, verbose_name='lien facebook')),
                ('twitter', models.URLField(blank=True, max_length=250, null=True, verbose_name='lien twitter')),
                ('linkedin', models.URLField(blank=True, max_length=250, null=True, verbose_name='lien linkedin')),
                ('instagramm', models.URLField(blank=True, max_length=250, null=True, verbose_name='lien instagramm')),
                ('is_staff', models.BooleanField(default=False, verbose_name='statut équipe')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='statut administrateur')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_buyer', models.BooleanField(default=False, verbose_name='statut acheteur')),
                ('is_seller', models.BooleanField(default=False, verbose_name='statut vendeur')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='date de derniere connexion')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name="date d'inscription")),
                ('slug', models.SlugField(blank=True, help_text='lien vers la boutique', verbose_name='URL de la boutique')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('interests', models.ManyToManyField(related_name='interested_customers', to='category.Category')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'utilisateur',
                'verbose_name_plural': 'utilisateurs',
                'ordering': ('-date_joined',),
                'index_together': {('email',)},
            },
        ),
    ]
