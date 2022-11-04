from django.shortcuts import render
from django.views import View


from .models import (
    Country,
    OrderItem,
    PaymentMethod,
    Region,
    City,
)
from .forms import OrderCreateForm
from cart.cart import CartLogic


class OrderCreate(View):
    def get(self, request):
        cart = CartLogic(request)
        form_create = OrderCreateForm()
        return render(
            request,
            "orders/order/create.html",
            context={
                "cart": cart,
                "form_create": form_create,
            },
        )

    def post(self, request):
        cart = CartLogic(request)
        data = request.POST
        form_create = OrderCreateForm(data)
        if form_create.is_valid():
            order = form_create.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            request.session["counter_items"] = 0
            return render(request, "orders/order/created.html", {"order": order})


def get_country(request):
    delivery_method_id = request.GET.get("method")
    countries = Country.objects.filter(method=delivery_method_id).order_by("country")
    return render(request, "selection/country.html", {"countries": countries})


def get_region(request):
    delivery_country_id = request.GET.get("country")
    regions = Region.objects.filter(country=delivery_country_id).order_by("region")
    return render(request, "selection/regions.html", {"regions": regions})


def get_city(request):
    delivery_region_id = request.GET.get("region")
    cities = City.objects.filter(region=delivery_region_id).order_by("city")
    return render(request, "selection/cities.html", {"cities": cities})


def get_pay_method(request):
    pay_method_id = request.GET.get("pay_method")
    pay_methods = PaymentMethod.objects.filter(delivery_method=pay_method_id).order_by(
        "method"
    )
    return render(request, "selection/pay_methods.html", {"pay_methods": pay_methods})
