# Generated by Django 3.1.5 on 2021-01-26 03:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20210126_0139'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='productreview',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='productreview',
            name='created_hour_at',
            field=models.TimeField(auto_now_add=datetime.datetime(2021, 1, 26, 3, 21, 13, 912792, tzinfo=utc)),
        ),
    ]
