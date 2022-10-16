from django.db import models
from allauth.utils import get_user_model
from ecomm.models import Product
from django.db.models.signals import m2m_changed, pre_save, post_save

User = get_user_model()


class CartManager(models.Manager):

    def new_or_get(self, request):
        card_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=card_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None, products=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(decimal_places=2, default=0.0, max_digits=100)
    total = models.DecimalField(decimal_places=2, default=0.0, max_digits=100)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()

    def __str__(self):
        return str(self.pk)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
            if instance.subtotal != total:
                instance.subtotal = total
                instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)


