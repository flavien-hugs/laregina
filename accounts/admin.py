from django.contrib import admin


from accounts.models import UserProfile, StoreProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(StoreProfile)