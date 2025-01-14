# Generated by Django 3.2.12 on 2023-07-02 10:03
import django.db.models.deletion
import mptt.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("category", "0001_initial"),
        ("catalogue", "0002_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=mptt.fields.TreeForeignKey(
                help_text="Selectionner la catégorie du produit.",
                on_delete=django.db.models.deletion.CASCADE,
                to="category.category",
                verbose_name="catégorie",
            ),
        ),
    ]
