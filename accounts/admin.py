# acccounts.admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from accounts.forms import MarketSignupForm, MarketChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = MarketSignupForm
    form = MarketChangeForm
    model = User

    fieldsets = (
        (None, {'fields':
            (
                "name",
                "email",
                "store",
                "phone_number",
                "whatsapp_number",
                "country",
                "city",
                "address",
                "facebook",
                "linkedin",
                "instagramm",
                "password",
                "last_login",
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
                'fields': ('email', 'password1', 'password2', 'is_staff', 'is_staff')
            }
        ),
    )

    list_display = (
        "email",
        "name",
        "store",
        "phone_number",
        "whatsapp_number",
        "country",
        "city",
        "address",
        "facebook",
        "linkedin",
        "instagramm",
        "is_buyer",
        "is_seller",
        "is_active",
        "last_login",
    )

    list_filter = (
        "is_buyer",
        "is_seller",
        "is_active",
        "last_login",
        "groups",
    )

    list_editable = (
        "is_active",
        "is_buyer",
        "is_seller",
    )

    search_fields = ('email', 'user', 'store',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
