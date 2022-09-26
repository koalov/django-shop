from django.urls import path
from . import views


app_name = 'ecomm'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('something/', views.something, name='something'),
    path('category/<slug:slug>/', views.category_page, name='category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]