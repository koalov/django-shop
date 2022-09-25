from django.urls import path
from . import views


app_name = 'ecomm'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.homepage, name='home'),
    path('feedback/', views.feedback, name='feedback'),
    path('something/', views.something, name='something'),
    path('category/<slug:cat_slug>/', views.homepage, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]