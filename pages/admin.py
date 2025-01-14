from django.contrib import admin
from pages import models
from services.export_data_csv import export_to_csv


@admin.register(models.HomePage)
class HomePageAdmin(admin.ModelAdmin):
    actions = None
    list_display = ["id", "page", "date"]
    empty_value_display = "-empty-"
    list_display_links = ["id"]
    list_editable = ["page"]
    readonly_fields = ["page"]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = ["full_name", "company", "email", "phone", "subject", "date"]

    list_filter = ["timestamp", "subject", "company"]

    list_per_page = 50
    empty_value_display = "-empty-"
    search_fields = ["subject", "email", "company"]
    list_display_links = ("email", "full_name")
    readonly_fields = (
        "timestamp",
        "full_name",
        "company",
        "phone",
        "email",
        "subject",
        "message",
    )
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False


class PromotionStackedInline(admin.StackedInline):
    model = models.Promotion
    extra = 0
    fieldsets = (
        (
            "Produit dans cette promotions",
            {
                "classes": ("collapse",),
                "fields": ("user", "campaign", "products", "is_active"),
            },
        ),
    )
    list_display = [
        "user",
        "campaign",
        "products",
        "get_products_count",
        "date",
    ]
    list_filter = ["user", "campaign"]
    list_per_page = 10
    verbose_name_plural = "Promotions"
    list_display_links = (
        "user",
        "campaign",
    )
    empty_value_display = "-empty-"


@admin.register(models.Campaign)
class CampaignAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "produit en promotions",
            {
                "classes": ("collapse",),
                "fields": (
                    "name",
                    "parent",
                    "discount",
                    "image",
                    "activate_at",
                ),
            },
        ),
    )
    list_display = [
        "__str__",
        "parent",
        "get_vouchers",
        "get_campaigns_count",
        "date",
        "show_image_tag",
        "activate_at",
    ]
    list_per_page = 10
    list_display_links = ("__str__",)
    empty_value_display = "-empty-"
    inlines = [PromotionStackedInline]


@admin.register(models.Pub)
class PubAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "name",
        "is_active",
        "date",
    ]
    fieldsets = (
        (
            "Publicité",
            {"classes": ("collapse",), "fields": ("name", "video", "is_active")},
        ),
    )
    list_per_page = 10
    empty_value_display = "-empty-"
    list_display_links = ("name",)


@admin.register(models.Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "name",
        "is_active",
        "date",
        "show_image_tag",
    ]
    fieldsets = (
        (
            "Publicité",
            {"classes": ("collapse",), "fields": ("name", "image", "is_active")},
        ),
    )
    list_per_page = 10
    empty_value_display = "-empty-"
    list_display_links = ("name",)


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "full_name",
        "status_client",
        "date",
    ]
    list_per_page = 10
    empty_value_display = "-empty-"
    list_display_links = ("full_name",)
    actions = [export_to_csv]
    exclude = ["created_at"]
