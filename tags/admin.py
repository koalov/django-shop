from django.contrib import admin
from .models import Tag

admin.site.register(Tag, prepopulated_fields={"slug": ("name",)})
