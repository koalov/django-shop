from django.db import models
from ecomm.models import Product

# from django.utils.translation import gettext_lazy as _


class DeliveryMethod(models.Model):
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.method}"


class Country(models.Model):
    method = models.ManyToManyField(DeliveryMethod)
    country = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.country}"


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.region}"


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.city}"


class PostOfficeNumber(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    post_office_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.post_office_number}"


class DeliveryAddress(models.Model):
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    post_office_no = models.ForeignKey(PostOfficeNumber, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.post_office_no}"


class PaymentMethod(models.Model):
    delivery_method = models.ManyToManyField(DeliveryMethod)
    method = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.method}"


class Order(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(
        DeliveryAddress, blank=True, null=True, on_delete=models.CASCADE
    )
    delivery_country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE
    )
    delivery_region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE
    )
    delivery_city = models.ForeignKey(
        City, blank=True, null=True, on_delete=models.CASCADE
    )
    post_office_number = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.pk}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
