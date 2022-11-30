# Generated by Django 3.2.12 on 2022-11-29 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_remove_distributorcustomer_ip_address"),
    ]

    operations = [
        migrations.AlterField(
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
    ]
