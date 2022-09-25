from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from cart.form import CartAddProductForm
from shop.settings import GOOGLE_MAPS_API_KEY

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'feedback'},
        {'title': "Что-то ещё", 'url_name': 'something'},
        {'title': "Корзина", 'url_name': 'cart'},
        ]


def homepage(request, cat_slug=None):
    category = None
    categories = Category.objects.all()
    # categories = Category.objects.filter(level=0)
    # categories = Category.get_children()

    products = Product.objects.filter(available=True)
    if cat_slug:
        category = get_object_or_404(categories, slug=cat_slug)
        products = products.filter(category=category)
    context = {'menu': menu,
               'products': products,
               'category': category,
               'categories': categories,
               'title': 'Главная страница',
               }
    return render(request, 'ecomm/main.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    product_spec = ProductSpecification.objects.all()
    product_spec_val = ProductSpecificationValue.objects.all()
    cart_product_form = CartAddProductForm()
    context = {'menu': menu,
               'product_spec': product_spec,
               'product_spec_val': product_spec_val,
               'product': product,
               'cart_product_form': cart_product_form}

    return render(request, 'ecomm/product.html', context=context)


def feedback(request):
    return render(request, 'ecomm/feedback.html', {'menu': menu,
                                                   'title': 'Обратная связь',
                                                   'api-key': GOOGLE_MAPS_API_KEY})


def something(request):
    return render(request, 'ecomm/something.html', {'menu': menu, 'title': 'Что то полезное'})


def about(request):
    return render(request, 'ecomm/about.html', {'menu': menu, 'title': 'О сайте'})


