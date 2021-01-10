# catalogue.admin.py

from django.contrib import admin

from catalogue.models import Product, ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)