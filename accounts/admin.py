# acccounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, Customer
from services.export_data_csv import export_to_csv
from accounts.forms import MarketSignupForm, MarketChangeForm

admin.site.site_header = "Laregina"
admin.site.site_title = "Laregina"
admin.site.index_title = "Espace d'Administration Laregina"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = MarketSignupForm
    form = MarketChangeForm
    model = User
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
        "email",
        "is_seller",
        "is_active",
        "last_login",
    )

    list_filter = (
        "is_seller",
        "is_active",
        ('is_staff', admin.BooleanFieldListFilter),
        "last_login",
    )

    list_editable = (
        "is_active",
        "is_seller",
    )

    list_per_page = 5
    list_display_links = ('store_id',  'store', 'email')
    prepopulated_fields = {'slug': ('store',)}
    search_fields = ('email', 'user', 'store',)
    ordering = ('date_joined',)
    actions = [export_to_csv]


@admin.register(Customer)
class CustomerEmailAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    model = Customer

    list_display = (
        "get_fullname",
        "email",
        "active",
        "created_at",
    )

    list_per_page = 5
    list_display_links = ('email',)
    search_fields = ['email']
    actions = [export_to_csv]