# Generated by Django 3.2.12 on 2023-07-02 10:59
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="activate_at",
            field=models.BooleanField(
                default=False, verbose_name="campagne disponible ?"
            ),
        ),
    ]
