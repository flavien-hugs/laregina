# Generated by Django 3.1.5 on 2021-01-21 08:23

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
            name='ProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=225, verbose_name='adresse ip')),
                ('tracking_id', models.CharField(db_index=True, default='', max_length=50)),
                ('date_viewed_at', models.DateField(auto_now=True, verbose_name='date de visite')),
                ('time_viewed_at', models.TimeField(auto_now=True, verbose_name='date de visite')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'statistique',
                'abstract': False,
            },
        ),
    ]