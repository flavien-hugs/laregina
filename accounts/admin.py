# acccounts.admin.py
from accounts.models import DistributorCustomer
from accounts.models import ProfileSocialMedia
from catalogue.models import Product
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from services.export_data_csv import export_to_csv


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    max_num = 1
    verbose_name = "produits"
    show_change_link = True
    list_display = ["name", "price"]
    exclude = [
        "updated_at",
        "created_at",
        "description",
        "keywords",
        "is_external",
        "slug",
        "quantity",
    ]


class UserSocialProfile(admin.TabularInline):
    extra = 1
    max_num = 1
    model = ProfileSocialMedia


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    date_hierarchy = "date_joined"
    fieldsets = (
        (
            "information sur la boutique",
            {
                "fields": (
                    ("store_id", "email"),
                    ("shipping_first_name", "shipping_last_name"),
                    "store",
                    ("is_seller", "is_active"),
                )
            },
        ),
        (
            "address de la boutique",
            {
                "classes": ("collapse",),
                "fields": [
                    ("shipping_country", "shipping_city"),
                    ("phone", "phone_two"),
                    "shipping_adress",
                ],
            },
        ),
        (
            "description de la boutique",
            {
                "classes": ("collapse",),
                "fields": ["store_description", "logo"],
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "is_staff")}),)
    list_display = (
        "get_vendor_logo",
        "store_id",
        "store",
        "email",
        "products",
        "last_login",
        "show_vendor_url",
    )
    list_filter = (
        "last_login",
        "date_joined",
    )
    list_per_page = 10
    list_display_links = (
        "store_id",
        "email",
    )
    readonly_fields = ["store_id", "show_vendor_url", "last_login", "date_joined"]

    actions = [export_to_csv]
    inlines = [ProductInline, UserSocialProfile]

    @mark_safe
    @admin.display(description="Voir la boutique", empty_value="???")
    def show_vendor_url(self, instance):
        if instance.is_seller:
            url = instance.get_absolute_url()
            response = format_html(
                f"""<a target="_blank" href="{url}!r">
                Afficher
                </a>"""
            )
            return response
        return "Aucun lien"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        vendors = qs.exclude(is_superuser=True)
        return vendors

    def has_add_permission(self, request):
        return False


@admin.register(DistributorCustomer)
class DistributorCustomerAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    fk_name = "product"
    readonly_fields = [
        "delivery_id",
        "gender",
        "fullname",
        "birth_date",
        "marital_status",
        "nationnality",
        "level_of_education",
        "profession",
        "commune",
        "district",
        "local_market",
        "phone",
        "phone_two",
        "shipping_city",
        "id_card_number",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "delivery_id",
        "get_fullname",
        "phone",
        "shipping_city",
        "date",
        "active",
    ]
    list_filter = ["created_at"]
    list_display_links = (
        "delivery_id",
        "get_fullname",
    )
    list_editable = ("active",)
