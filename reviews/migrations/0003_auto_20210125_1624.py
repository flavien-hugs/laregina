# Generated by Django 3.1.5 on 2021-01-25 16:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20210125_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='created_hour_at',
            field=models.TimeField(auto_now_add=datetime.datetime(2021, 1, 25, 16, 24, 15, 985105, tzinfo=utc)),
        ),
    ]