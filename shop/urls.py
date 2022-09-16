"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from ecomm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^cart/', include('cart.urls')),
    path('about/', views.about, name='about'),
    path('', views.homepage, name='home'),
    path('product/<slug:prod_slug>/', views.product_page, name='product'),
    path('feedback/', views.feedback, name='feedback'),
    path('something/', views.something, name='something'),
    path('login/', views.login, name='login'),
    path('basket/<pk>/', views.basket, name='basket'),
    path('<slug:cat_slug>/', views.category_page, name='category'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)