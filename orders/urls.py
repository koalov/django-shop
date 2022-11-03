from django.urls import re_path, path
from . import views


urlpatterns = [
    re_path(r"^create/$", views.OrderCreate.as_view(), name="order_create"),
    path("ajax/load_country", views.get_country, name="ajax_load_countries"),
    path("ajax/load_regions", views.get_region, name="ajax_load_regions"),
    path("ajax/load_cities", views.get_city, name="ajax_load_cities"),
    path("ajax/load_pay_methods", views.get_pay_method, name="ajax_load_pay_methods"),
]
