# acccounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, GuestCustomer
from services.export_data_csv import export_to_csv
from accounts.forms import MarketSignupForm, MarketChangeForm

admin.site.site_header = "Laregina"
admin.site.site_title = "Laregina"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = MarketSignupForm
    fieldsets = (
        (None, {'fields':
            (   
                "store_id",
                "store",
                "shipping_first_name",
                "shipping_last_name",
                "email",
                "slug",
                "phone",
                "phone_two",
                "shipping_country",
                "shipping_city",
                "store_description",
                "shipping_adress",
            )}
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'slug',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )
    list_display = (
        "store_id",
        "store",
        "last_login",
        "is_active",
    )

    list_filter = (
        "is_active",
        "last_login",
    )

    list_editable = (
        "is_active",
    )

    list_per_page = 5
    list_display_links = (
        'store_id',
        'store',
    )
    prepopulated_fields = {'slug': ('store',)}
    search_fields = ('email', 'user', 'store',)
    ordering = ('date_joined',)
    actions = [export_to_csv]

admin.site.register(GuestCustomer)
