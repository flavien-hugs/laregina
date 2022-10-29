# Generated by Django 3.2.12 on 2022-10-29 05:26

import django.core.validators
from django.db import migrations, models
import helpers.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['date_joined'], 'verbose_name_plural': 'boutiques'},
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(blank=True, help_text='Ajouter le logo de votre boutique', null=True, upload_to=helpers.utils.upload_image_logo_path, validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png'])], verbose_name='logo'),
        ),
    ]
