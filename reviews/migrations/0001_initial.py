# Generated by Django 3.1.6 on 2021-02-20 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, verbose_name='note')),
                ('content', models.TextField(verbose_name='avis client')),
                ('created_time_at', models.DateField(auto_now_add=True)),
                ('created_hour_at', models.TimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False, verbose_name='approuvé ?')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.product', verbose_name='produit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='client')),
            ],
            options={
                'verbose_name_plural': 'avis des clients',
                'db_table': 'reviews_db',
                'ordering': ['-rating', '-created_time_at', '-created_time_at'],
                'get_latest_by': ['-created_time_at', '-created_time_at', '-rating'],
                'unique_together': {('product',)},
                'index_together': {('product',)},
            },
        ),
    ]
