from django.urls import path

from . import views

app_name = 'send_email'

urlpatterns = [
    path('send_mail', views.mail_send, name='send_email')
]