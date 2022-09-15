from django.contrib import admin
from ecomm.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'image', 'image_img', 'available', 'price')
    readonly_fields = ['image_img', ]
    list_display_links = ('id', 'name')
    search_fields = ('name', 'price')
    list_filter = ('available', 'created')
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'available')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('available',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    pass
