from django.contrib import admin

from mainapp.models import ProductCategory, Products

# Register your models here.
admin.site.register(Products)
admin.site.register(ProductCategory)
