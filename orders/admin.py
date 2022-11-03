from django.contrib import admin
from .models import (
    Country,
    Region,
    City,
    PostOfficeNumber,
    OrderItem,
    Order,
    DeliveryMethod,
    DeliveryAddress,
    PaymentMethod,
)

admin.site.register(DeliveryMethod)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(PostOfficeNumber)
admin.site.register(DeliveryAddress)
admin.site.register(PaymentMethod)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


class DeliveryAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "delivery_method",
        "delivery_address",
        "payment_method",
        "paid",
        "created_at",
        "updated_at",
    ]
    list_filter = ["paid", "created_at", "updated_at"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
