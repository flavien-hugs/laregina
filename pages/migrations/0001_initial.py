# Generated by Django 3.2.8 on 2021-10-21 08:50

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nom & prénoms')),
                ('email', models.EmailField(max_length=150, verbose_name='email')),
                ('phone', models.CharField(max_length=150, verbose_name='téléphone')),
                ('subject', models.CharField(max_length=150, verbose_name='sujet de la requete')),
                ('company', models.CharField(blank=True, max_length=150, null=True, verbose_name='entreprise')),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
            ],
            options={
                'verbose_name_plural': 'messages',
                'db_table': 'contact_db',
                'ordering': ['-timestamp'],
                'get_latest_by': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Entrer le nom et prénoms du client', max_length=120, verbose_name='nom & prénoms')),
                ('status_client', models.CharField(blank=True, help_text='Entrer le statut du client', max_length=120, null=True, verbose_name='Statut (entrepreneur/boutique/etc)')),
                ('message', models.TextField(help_text='Entrer le message du client', verbose_name='message')),
                ('image', models.ImageField(blank=True, null=True, upload_to='testimonial_image/', verbose_name='image')),
                ('created_at', models.DateField(auto_now=True, verbose_name='date')),
                ('activate_at', models.BooleanField(default=False, help_text='rendre visible cet témoignage ?', verbose_name='actif')),
            ],
            options={
                'verbose_name_plural': 'Témoignage',
                'db_table': 'testimonial_db',
                'ordering': ['-created_at'],
                'get_latest_by': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Titre de la promotion')),
                ('slug', models.SlugField(blank=True, verbose_name='lien')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_promotion_image_path, verbose_name='image')),
                ('active', models.BooleanField(default=False, verbose_name='promotion active ?')),
                ('created_at', models.DateField(auto_now=True, verbose_name='date de creation')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category', verbose_name='promotion')),
            ],
            options={
                'verbose_name_plural': 'promotion',
                'db_table': 'promotion_db',
                'ordering': ['-created_at'],
                'get_latest_by': ['-created_at'],
            },
        ),
    ]
