from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST


from ecomm.models import Product
from .cart import CartLogic
from .form import CartAddProductForm


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
    return redirect('ecomm:product_detail', product_id, product.slug)


def cart_remove(request, product_id):
    cart = CartLogic(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = CartLogic(request)
    return render(request, 'cart/detail.html', {'cart': cart})

