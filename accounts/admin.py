# acccounts.admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from accounts.forms import MarketSignupForm, MarketChangeForm

admin.site.site_header = "CGIC MARKET"
admin.site.site_title = "CGIC MARKET Admin"
admin.site.index_title = "Espace d'Administration CGIC MARKET"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = MarketSignupForm
    form = MarketChangeForm
    model = User

    fieldsets = (
        (None, {'fields':
            (   
                "store_id",
                "name",
                "email",
                "store",
                "slug",
                "phone_number",
                "whatsapp_number",
                "country",
                "city",
                "store_description",
                "address",
                "facebook",
                "linkedin",
                "instagramm",
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

    prepopulated_fields = {'slug': ('store',)}
    search_fields = ('email', 'user', 'store',)
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
