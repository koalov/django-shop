from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

from shop.utils import unique_slug_generator
from ecomm.models import Product


class Tag(models.Model):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    slug = models.SlugField(verbose_name=_("Slug"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Time stamp"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    products = models.ManyToManyField(Product, blank=True, verbose_name=_("Products"))

    def __str__(self):
        return self.name


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
