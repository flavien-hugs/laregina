# Generated by Django 3.1.7 on 2021-02-24 03:32

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Le nom du produit', max_length=120, verbose_name='nom du produit')),
                ('quantity', models.PositiveIntegerField(default=1, help_text='quantité de produit', verbose_name='quantité')),
                ('price', models.DecimalField(decimal_places=0, default=0, help_text='Le prix du produit', max_digits=50, verbose_name='prix de vente')),
                ('description', models.TextField(help_text='Définir votre produit.', verbose_name='description du produit')),
                ('keywords', models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for keywords meta tag', max_length=50, verbose_name='mots clés')),
                ('is_external', models.BooleanField(default=False, help_text='Ce produit peut-être livrer en dehors de votre pays ?', verbose_name='Ce produit peut-être livrer en dehors de votre pays ?')),
                ('is_active', models.BooleanField(default=True, help_text='ce produit est-il disponible ?', verbose_name='produit disponible ?')),
                ('slug', models.SlugField(blank=True, help_text='Unique value for product page URL, created automatically from name.', verbose_name='URL du produit')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="date d'ajout automatique du produit", verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='date de mise à jour automatique du produit.', verbose_name='date de mise à jour')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', mptt.fields.TreeForeignKey(help_text='Selectionner la catégorie du produit.', on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='catégorie')),
                ('user', models.ForeignKey(help_text='Le magasin en charge de la vente.', limit_choices_to={'is_seller': True, 'is_staff': True, 'is_superuser': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='vendeur')),
            ],
            options={
                'verbose_name_plural': 'catalogue',
                'db_table': 'catalogue_db',
                'ordering': ['-created_at', '-updated_at', '-timestamp'],
                'get_latest_by': ['-created_at', '-updated_at', '-timestamp'],
                'unique_together': {('slug',)},
                'index_together': {('slug',)},
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Taille: 300x300px', upload_to=core.utils.upload_image_path, verbose_name='image du produit')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='image produit')),
            ],
            options={
                'verbose_name_plural': 'images du produit',
                'db_table': 'product_image_db',
                'ordering': ['-updated', '-timestamp'],
            },
        ),
    ]
