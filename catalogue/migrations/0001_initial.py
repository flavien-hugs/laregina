# Generated by Django 3.2.12 on 2022-10-29 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import helpers.utils
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Le nom du produit', max_length=255, verbose_name='nom du produit')),
                ('quantity', models.PositiveIntegerField(default=1, help_text='quantité de produit', verbose_name='quantité')),
                ('price', models.DecimalField(decimal_places=0, default=0, help_text='Le prix du produit', max_digits=50, verbose_name='prix de vente')),
                ('description', models.TextField(help_text='Définir votre produit.', verbose_name='description du produit')),
                ('keywords', models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for keywords meta tag', max_length=50, verbose_name='mots clés')),
                ('is_external', models.BooleanField(default=False, help_text='Ce produit peut-être livrer en dehors de votre pays ?', verbose_name='Ce produit peut-être livrer en dehors de votre pays ?')),
                ('is_active', models.BooleanField(default=True, help_text='ce produit est-il disponible ?', verbose_name='produit disponible ?')),
                ('slug', models.SlugField(blank=True, help_text='Unique value for product page URL, created automatically from name.', unique=True, verbose_name='URL du produit')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', mptt.fields.TreeForeignKey(help_text='Selectionner la catégorie du produit.', on_delete=django.db.models.deletion.PROTECT, to='category.category', verbose_name='catégorie')),
                ('user', models.ForeignKey(help_text='magasin en charge de la vente.', limit_choices_to={'is_seller': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='vendeur')),
            ],
            options={
                'verbose_name_plural': 'produits',
                'db_table': 'catalogue_db',
                'ordering': ['-created_at', '-updated_at', '-timestamp'],
                'get_latest_by': ['-created_at', '-updated_at', '-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Taille: 300x300px', upload_to=helpers.utils.upload_image_path, verbose_name='image du produit')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='image produit')),
            ],
            options={
                'verbose_name_plural': 'galleries du produit',
                'db_table': 'product_image_db',
                'ordering': ['-updated', '-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='M', help_text='Sélectionner une taille', max_length=2, verbose_name='tailles')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='attribut')),
            ],
            options={
                'verbose_name_plural': 'Tailles',
            },
        ),
        migrations.AddIndex(
            model_name='productattributevalue',
            index=models.Index(fields=['id'], name='catalogue_p_id_6294c9_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id'], name='id_index_product'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('slug',)},
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('slug',)},
        ),
    ]
