# reviews.admin.py

from django.contrib import admin

from reviews.models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("email", "product", "rating", "content", "is_approved")
    list_filter = ("is_approved", "created_time_at", "created_hour_at")
    search_fields = ("content", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    def has_add_permission(self, request):
        return False
