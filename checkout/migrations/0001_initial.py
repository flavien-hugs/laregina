# Generated by Django 3.1.7 on 2021-02-25 22:59

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, verbose_name='adresse de messagerie')),
                ('shipping_first_name', models.CharField(max_length=50, verbose_name='nom de famille')),
                ('shipping_last_name', models.CharField(max_length=50, verbose_name='prénom')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='numéro de téléphone')),
                ('phone_two', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='téléphone supplémentaire (facultatif)')),
                ('shipping_city', models.CharField(max_length=50, verbose_name='ville')),
                ('shipping_country', django_countries.fields.CountryField(max_length=2, verbose_name='pays/région')),
                ('shipping_adress', models.CharField(max_length=50, verbose_name='situation géographique')),
                ('shipping_zip', models.CharField(blank=True, max_length=10, null=True, verbose_name='adresse postal (facultatif)')),
                ('note', models.TextField(blank=True, max_length=120, null=True, verbose_name='note de commande (facultatif)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Soumis', 'Soumis'), ('En cours de livraison', 'Commande en cours de livraison'), ('Commande reçue', 'Commande reçue'), ('Commande annulée', 'Commande annulée')], default='Soumis', max_length=26, verbose_name='status')),
                ('transaction_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='id de la commande')),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True, verbose_name='adresse ip')),
                ('emailing', models.BooleanField(default=False, verbose_name='abonnement aux offres et promotions')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date de la commade')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='derniere modification')),
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
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='derniere modification')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='date ajout')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.order', verbose_name='commande')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='produit')),
            ],
            options={
                'verbose_name_plural': 'panier',
                'db_table': 'checkout_order_item_db',
                'ordering': ['-date_created', '-date_updated'],
                'get_latest_by': ['-date_created', '-date_updated'],
            },
        ),
    ]