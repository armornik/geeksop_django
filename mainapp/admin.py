from django.contrib import admin

from mainapp.models import ProductCategory, Products

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    # list_display - какие поля отобразить
    list_display = ('name', 'price', 'quantity', 'category')
    # fields - в какой последовательности и какие поля показать
    # ('price', 'quantity') - отобразить на одной строке
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category')
    # readonly_fields - какие поля только для чтения
    readonly_fields = ('short_description',)
    # ordering - по какому полю сортировать (можно несколько полей)
    ordering = ('name', 'price')
    # search_fields - по какому полю производить поиск
    search_fields = ('name',)
