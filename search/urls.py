from django.urls import re_path
from .views import SearchProductView


urlpatterns = [
    re_path('', SearchProductView.as_view(), name='query')
]