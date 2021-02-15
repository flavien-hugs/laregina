# Generated by Django 3.1.6 on 2021-02-11 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0002_auto_20210211_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='external_delivery',
        ),
        migrations.AlterField(
            model_name='product',
            name='is_external',
            field=models.BooleanField(default=False, help_text='Ce produit peut-être livrer en dehors de votre pays ?', verbose_name='Ce produit peut-être livrer en dehors de votre pays ?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=50, verbose_name='prix normal'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, help_text='Le prix du produit', max_digits=50, verbose_name='prix de vente'),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(help_text='Le vendeur en charge du magasin', limit_choices_to={'is_seller': True, 'is_staff': True, 'is_superuser': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to=settings.AUTH_USER_MODEL, verbose_name='vendeur'),
        ),
    ]
