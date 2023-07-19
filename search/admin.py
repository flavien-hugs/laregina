from django.contrib import admin
from services.export_data_csv import export_to_csv


# @admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    date_hierarchy = "date_search_at"
    list_display_links = ("__str__",)
    list_filter = ("date_search_at", "ip_address", "user", "q")
    list_display = ("__str__", "ip_address", "date_search_at", "time_search_at")
    exclude = ("user",)
    readonly_fields = ("q", "ip_address", "date_search_at", "time_search_at")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False
