# Generated by Django 3.2.12 on 2022-12-01 13:41
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_auto_20221201_1332"),
        ("checkout", "0003_auto_20221201_1332"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="distributor",
            field=models.ForeignKey(
                blank=True,
                help_text="Choisir un livreur",
                limit_choices_to={"active": True},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="distibutors",
                to="accounts.distributorcustomer",
                verbose_name="livreur",
            ),
        ),
    ]
