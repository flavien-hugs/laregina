from accounts.models import DistributorCustomer
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from services.export_data_csv import export_to_csv


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    date_hierarchy = "last_login"
    fieldsets = (
        (
            "information sur l'utilisateur",
            {
                "fields": (
                    ("user_id", "email"),
                    ("firstname", "lastname"),
                    "description",
                    "avatar",
                    ("is_customer", "is_active"),
                )
            },
        ),
        (
            "address de la boutique",
            {
                "classes": ("collapse",),
                "fields": [
                    ("country", "city"),
                    ("phone", "phone_two"),
                ],
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "is_staff")}),)
    list_display = (
        "get_user_avatar",
        "user_id",
        "email",
        "last_login",
    )
    list_filter = (
        "last_login",
        "created_at",
    )
    list_per_page = 10
    list_display_links = (
        "user_id",
        "email",
    )
    readonly_fields = ["user_id", "last_login", "created_at"]

    actions = [export_to_csv]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        users = qs.exclude(is_superuser=True)
        return users

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
        "city",
        "id_card_number",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "delivery_id",
        "get_fullname",
        "phone",
        "city",
        "date",
        "active",
    ]
    list_filter = ["created_at"]
    list_display_links = (
        "delivery_id",
        "get_fullname",
    )
    list_editable = ("active",)
