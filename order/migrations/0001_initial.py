# Generated by Django 3.1.5 on 2021-01-21 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, verbose_name='adresse email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='numéro de téléphone')),
                ('shipping_first_name', models.CharField(max_length=50, verbose_name='nom de famille')),
                ('shipping_last_name', models.CharField(max_length=50, verbose_name='prénom')),
                ('shipping_address', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='+225xxxxxxxx', max_length=128, region=None, verbose_name='numéro de téléphone WhatsApp')),
                ('shipping_city', models.CharField(max_length=50, verbose_name='ville')),
                ('shipping_country', django_countries.fields.CountryField(max_length=2, verbose_name='pays')),
                ('shipping_zip', models.CharField(blank=True, max_length=10, verbose_name='adresse postal (optionnel)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date de la commade')),
                ('status', models.IntegerField(choices=[(1, 'Soumis'), (2, 'Traitée'), (3, 'Expédié'), (4, 'Annulé')], default=1, verbose_name='status de le commande')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='derniere modification')),
                ('transaction_id', models.CharField(max_length=20, verbose_name='id de la commande')),
                ('ip_address', models.CharField(max_length=50, verbose_name='adresse ip')),
                ('emailing', models.BooleanField(default=False, verbose_name='activer les offres')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='client')),
            ],
            options={
                'verbose_name_plural': 'commande',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantité')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='coût total')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='commande')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.product', verbose_name='produit')),
            ],
            options={
                'verbose_name_plural': 'panier',
            },
        ),
    ]
