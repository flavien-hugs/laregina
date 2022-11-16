# Generated by Django 3.2.12 on 2022-10-29 13:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Voucher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="date de création",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text="Activé/Désactivé ?",
                        verbose_name="Activé/Désactivé",
                    ),
                ),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="pourcentage de réduction",
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        help_text="Choisir des produits",
                        to="catalogue.Product",
                        verbose_name="produits",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        limit_choices_to={"is_seller": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="store",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "réductions produits",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="voucher",
            index=models.Index(fields=["id"], name="voucher_vou_id_d8b0d2_idx"),
        ),
    ]
