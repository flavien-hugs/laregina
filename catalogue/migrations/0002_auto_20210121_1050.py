# Generated by Django 3.1.5 on 2021-01-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='external_delivery',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=50, verbose_name='Prix de la livraison internationale'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, help_text='Le prix du produit', max_digits=50, verbose_name='prix'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, help_text='le prix du produit', max_digits=50, verbose_name='le prix du produit'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='sale_price',
            field=models.DecimalField(decimal_places=0, default=0, help_text='le prix du produit', max_digits=50, verbose_name='le prix de vente du produit'),
        ),
    ]
