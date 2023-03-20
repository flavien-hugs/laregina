# Generated by Django 3.2.12 on 2022-11-29 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_auto_20221129_0421"),
    ]

    operations = [
        migrations.AddField(
            model_name="distributorcustomer",
            name="delivery_id",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                unique=True,
                verbose_name="ID Distributeur",
            ),
        ),
        migrations.AddField(
            model_name="distributorcustomer",
            name="ip_address",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Adresse IP"
            ),
        ),
    ]