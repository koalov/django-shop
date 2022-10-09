from django.urls import path
from . import views

app_name = 'filter'

urlpatterns = [
    path('', views.filter_page, name='filter'),
]
