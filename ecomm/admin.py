from django.contrib import admin
from ecomm.models import *
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'name'),
    list_display_links=('indented_title',),
    search_fields=('name',),
    list_filter=('available',),
    prepopulated_fields={"slug": ("name",)}
)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline, ]


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationValueInline, ]
    list_display = ('id', 'name', 'created', 'image', 'image_img', 'available', 'price')
    readonly_fields = ['image_img', ]
    list_display_links = ('id', 'name')
    search_fields = ('name', 'price')
    list_filter = ('available', 'created', 'category')
    prepopulated_fields = {"slug": ('name',)}
