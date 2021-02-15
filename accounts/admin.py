# acccounts.admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from accounts.forms import MarketSignupForm, MarketChangeForm

admin.site.site_header = "Laregina"
admin.site.site_title = "Laregina"
admin.site.index_title = "Espace d'Administration Laregina"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = MarketSignupForm
    form = MarketChangeForm
    model = User

    fieldsets = (
        (None, {'fields':
            (   
                "store_id",
                "shipping_first_name",
                "shipping_last_name",
                "email",
                "store",
                "slug",
                "phone",
                "phone_two",
                "shipping_country",
                "shipping_city",
                "store_description",
                "shipping_adress",
                "password",
            )}
        ),

        ('Permissions', {'fields': (
            'is_active', 
            'is_staff',
            'groups', 
            'user_permissions',
        )}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'slug', 'password1', 'password2', 'is_staff', 'is_active')
            }
        ),
    )

    list_display = (
        "store_id",
        "email",
        "store",
        "is_buyer",
        "is_seller",
        "is_active",
        "last_login",
    )

    list_filter = (
        "is_buyer",
        "is_seller",
        "is_active",
        ('is_staff', admin.BooleanFieldListFilter),
        "last_login",
        "groups",
    )

    list_editable = (
        "is_active",
        "is_buyer",
        "is_seller",
    )

    list_display_links = ('store_id', 'email', 'store')
    prepopulated_fields = {'slug': ('store',)}
    search_fields = ('email', 'user', 'store',)
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)

