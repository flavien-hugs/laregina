# Generated by Django 3.2.8 on 2021-10-21 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(db_index=True, max_length=50, verbose_name='ID PANIER')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantité')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="date d'ajout")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de mise à jour')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='produit')),
            ],
            options={
                'verbose_name_plural': 'panier',
                'db_table': 'cart_items_db',
                'ordering': ('-created_at', '-updated_at', '-cart_id'),
                'get_latest_by': ('-created_at', '-updated_at', '-cart_id'),
                'index_together': {('cart_id',)},
            },
        ),
    ]
