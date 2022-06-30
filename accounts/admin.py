# acccounts.admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from accounts.models import ProfileSocialMedia
from services.export_data_csv import export_to_csv

admin.site.unregister(Site)
admin.site.unregister(Group)


class UserSocialProfile(admin.TabularInline):
    extra = 1
    max_num = 1
    model = ProfileSocialMedia
    show_change_link = True


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    model = get_user_model()
    form = UserChangeForm
    date_hierarchy = 'date_joined'
    fieldsets = (
        ('information sur la boutique', {'fields':
            (
                ("store_id", "email"),
                "store",
                ("shipping_first_name", "shipping_last_name"),
            )}
        ),
        (
            'address de la boutique',
            {
                'classes': ('collapse',),
                'fields': [
                    ('shipping_country', "shipping_city"),
                    ("phone", "phone_two"),
                    "shipping_adress",
                ],
            }
        ),
        (
            'description de la boutique',
            {
                'classes': ('collapse',),
                'fields': ["store_description", "logo"],
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'is_staff',
                    'account_verified'
                )
            }
        ),
    )
    list_display = (
        "get_vendor_logo",
        "store_id",
        "store",
        "email",
        "last_login",
        "date_joined",
        "account_verified",
        "show_vendor_url"
    )
    list_filter = (
        "last_login",
        "date_joined",
    )
    list_per_page = 10
    list_display_links = (
        'store_id',
        'email',
    )
    search_fields = ('email', 'user', 'store',)
    readonly_fields = ['store_id', 'show_vendor_url', 'last_login', 'date_joined']

    actions = [export_to_csv]
    inlines = [UserSocialProfile]

    @mark_safe
    @admin.display(description="Voir la boutique", empty_value="???")
    def show_vendor_url(self, instance):
        if instance.is_seller:
            url = instance.get_absolute_url()
            response = format_html(
                f"""<a target="_blank" href="{url}">
                Afficher
                </a>"""
            )
            return response
        else:
            return "Aucun lien"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        vendors = qs.filter(is_seller=True)
        return  vendors
