# Generated by Django 3.2.12 on 2022-10-29 13:45
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import helpers.utils
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Annonce",
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
                    "name",
                    models.CharField(
                        help_text="Saisir le titre de la publicité",
                        max_length=225,
                        verbose_name="Titre",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=helpers.utils.upload_campign_image_path,
                        verbose_name="image",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="actif/inactif ?"),
                ),
            ],
            options={
                "verbose_name_plural": "Annonces",
                "db_table": "annonce_db",
                "ordering": ["-created_at"],
                "get_latest_by": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Campaign",
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
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Automatiquement formé à partir du nom.",
                        max_length=225,
                        null=True,
                        unique=True,
                        verbose_name="URL de la boutique",
                    ),
                ),
                (
                    "parent",
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True,
                        verbose_name="titre de la campagne",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Destockage", "Destockage"),
                            ("Vente Flash", "Vente Flash"),
                            ("Nouvel Arrivage", "Nouvel Arrivage"),
                        ],
                        default="Vente Flash",
                        max_length=120,
                        null=True,
                        verbose_name="campagne",
                    ),
                ),
                (
                    "discount",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="pourcentage de réduction",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=helpers.utils.upload_campign_image_path,
                        verbose_name="image",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Campagnes",
                "ordering": ["-created_at"],
                "get_latest_by": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Contact",
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
                    "full_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Nom & prénoms",
                    ),
                ),
                ("email", models.EmailField(max_length=150, verbose_name="email")),
                ("phone", models.CharField(max_length=150, verbose_name="téléphone")),
                (
                    "subject",
                    models.CharField(
                        max_length=150, verbose_name="sujet de la requete"
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="entreprise"
                    ),
                ),
                ("message", models.TextField(verbose_name="message")),
                (
                    "timestamp",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="date",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "messages",
                "db_table": "contact_db",
                "ordering": ["-timestamp"],
                "get_latest_by": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="HomePage",
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
                    "page",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Page par défaut"),
                            (1, "Page Supermarché"),
                            (2, "Page Combinée"),
                        ],
                        default=0,
                        verbose_name="Page",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Accueil page",
            },
        ),
        migrations.CreateModel(
            name="Promotion",
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
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Automatiquement formé à partir du nom.",
                        max_length=225,
                        null=True,
                        unique=True,
                        verbose_name="URL de la boutique",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text="Activé/Désactivé ?",
                        verbose_name="Activé/Désactivé",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "promotions",
                "db_table": "promotion_db",
                "ordering": ["-created_at"],
                "get_latest_by": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Pub",
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
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Automatiquement formé à partir du nom.",
                        max_length=225,
                        null=True,
                        unique=True,
                        verbose_name="URL de la boutique",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Saisir le titre de la publicité",
                        max_length=225,
                        null=True,
                        verbose_name="Titre",
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        upload_to="videos/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "mp4",
                                    "webm",
                                    "flv",
                                    "mov",
                                    "ogv",
                                    "3gp",
                                    "3g2",
                                    "wmv",
                                    "mpeg",
                                    "flv",
                                    "mkv",
                                    "avi",
                                ]
                            )
                        ],
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="actif/inactif ?"),
                ),
            ],
            options={
                "verbose_name_plural": "Pubs Vidéos",
                "ordering": ["-created_at"],
                "get_latest_by": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Testimonial",
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
                    "full_name",
                    models.CharField(
                        help_text="Entrer le nom et prénoms du client",
                        max_length=120,
                        verbose_name="nom & prénoms",
                    ),
                ),
                (
                    "status_client",
                    models.CharField(
                        blank=True,
                        help_text="Entrer le statut du client",
                        max_length=120,
                        null=True,
                        verbose_name="Statut (entrepreneur/boutique/etc)",
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        help_text="Entrer le message du client", verbose_name="message"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="testimonial_image/",
                        verbose_name="image",
                    ),
                ),
                (
                    "activate_at",
                    models.BooleanField(
                        default=False,
                        help_text="rendre visible cet témoignage ?",
                        verbose_name="actif",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Témoignages",
                "db_table": "testimonial_db",
                "ordering": ["-created_at"],
                "get_latest_by": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="testimonial",
            index=models.Index(fields=["id"], name="testimonial_id_f4eb67_idx"),
        ),
        migrations.AddIndex(
            model_name="pub",
            index=models.Index(fields=["id"], name="pages_pub_id_37cd35_idx"),
        ),
        migrations.AddField(
            model_name="promotion",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="campaigns",
                to="pages.campaign",
                verbose_name="campagne",
            ),
        ),
        migrations.AddField(
            model_name="promotion",
            name="products",
            field=models.ManyToManyField(
                help_text="Choisir des produits",
                to="catalogue.Product",
                verbose_name="produits",
            ),
        ),
        migrations.AddField(
            model_name="promotion",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={"is_seller": True},
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="store",
            ),
        ),
        migrations.AddIndex(
            model_name="homepage",
            index=models.Index(fields=["id"], name="pages_homep_id_f2366e_idx"),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(fields=["id"], name="contact_db_id_53481b_idx"),
        ),
        migrations.AddIndex(
            model_name="campaign",
            index=models.Index(fields=["id"], name="pages_campa_id_26598f_idx"),
        ),
        migrations.AddIndex(
            model_name="annonce",
            index=models.Index(fields=["id"], name="annonce_db_id_efcc47_idx"),
        ),
        migrations.AddIndex(
            model_name="promotion",
            index=models.Index(fields=["id"], name="promotion_d_id_d42a30_idx"),
        ),
    ]
