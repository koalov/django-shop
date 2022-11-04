from django.urls import path
from .views import profile, profile_update

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),

]
