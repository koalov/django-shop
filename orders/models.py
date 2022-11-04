from django.db import models
from django.utils.translation import gettext_lazy as _

from ecomm.models import Product


class DeliveryMethod(models.Model):
    method = models.CharField(max_length=50, verbose_name=_("Method"))

    def __str__(self):
        return f"{self.method}"


class Country(models.Model):
    method = models.ManyToManyField(DeliveryMethod, verbose_name=_("Method"))
    country = models.CharField(max_length=128, verbose_name=_("Country"))

    def __str__(self):
        return f"{self.country}"


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                verbose_name=_("Country"))
    region = models.CharField(max_length=128, verbose_name=_("Region"))

    def __str__(self):
        return f"{self.region}"


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               verbose_name=_("Region"))
    city = models.CharField(max_length=150, verbose_name=_("City"))

    def __str__(self):
        return f"{self.city}"


class PostOfficeNumber(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("City"))
    post_office_number = models.CharField(max_length=50,
                                          verbose_name=_("Post office number"))

    def __str__(self):
        return f"{self.post_office_number}"


class DeliveryAddress(models.Model):
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE,
                                        verbose_name=_("Delivery method"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                verbose_name=_("Country"))
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("City"))
    post_office_no = models.ForeignKey(PostOfficeNumber, on_delete=models.CASCADE,
                                       verbose_name=_("Post office number"))

    def __str__(self):
        return f"{self.country}, {self.city}, {self.post_office_no}"


class PaymentMethod(models.Model):
    delivery_method = models.ManyToManyField(DeliveryMethod,
                                             verbose_name=_("Delivery method"))
    method = models.CharField(max_length=80, verbose_name=_("Payment method"))

    def __str__(self):
        return f"{self.method}"


class Order(models.Model):

    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone number"))
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE,
                                        verbose_name=_("Delivery method"))
    delivery_address = models.ForeignKey(
        DeliveryAddress, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("Delivery address")
    )
    delivery_country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("Delivery address")
    )
    delivery_region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("Delivery region")
    )
    delivery_city = models.ForeignKey(
        City, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("Delivery city")
    )
    post_office_number = models.CharField(max_length=50, blank=True, null=True,
                                          verbose_name=_("Post office number"))
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE,
                                       verbose_name=_("Payment method"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    paid = models.BooleanField(default=False, verbose_name=_("Paid"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

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
        Product, related_name="order_items", on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name=_("Price"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
