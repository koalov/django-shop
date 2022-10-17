from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from ecomm.models import Product
from .cart import CartLogic
from .form import CartAddProductForm
# from .models import Cart


# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     return cart_obj


@require_POST
def cart_add(request, product_id):
    cart = CartLogic(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = CartLogic(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = CartLogic(request)
    return render(request, 'cart/detail.html', {'cart': cart})

