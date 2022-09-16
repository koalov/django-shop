from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from cart.form import CartAddProductForm


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'feedback'},
        {'title': "Что-то ещё", 'url_name': 'something'},
        # {'title': "Корзина", 'url_name': 'basket'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def about(request):
    return render(request, 'ecomm/about.html', {'menu': menu, 'title': 'О сайте'})


def homepage(request):
    list_products = Product.objects.all().values()
    category = Category.objects.all()
    context = {'menu': menu,
               'products': list_products,
               'category': category,
               'title': 'Главная страница'}

    return render(request, 'ecomm/main.html', context=context)


def product_page(request, prod_slug):
    product = Product.objects.get(slug=prod_slug)
    charcs = product.characteristics.all().values()
    cart_product_form = CartAddProductForm()

    context = {'menu': menu,
               'product': product,
               'charc': charcs,
               'title': 'Товар',
               'cart_product_form': cart_product_form}

    return render(request, 'ecomm/product.html', context=context)


def category_page(request, cat_slug):
    category = Category.objects.get(slug=cat_slug)
    product = category.product_set.all()
    context = {'menu': menu,
               'category': category,
               'product': product,
               'title': 'Категории'}

    return render(request, 'ecomm/category.html', context=context)


def feedback(request):
    return render(request, 'ecomm/feedback.html', {'menu': menu, 'title': 'Обратная связь'})


def login(request):
    return render(request, 'ecomm/login.html', {'menu': menu, 'title': 'Личный кабинет'})


def basket(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'ecomm/basket.html', {'menu': menu, 'title': 'Корзина', 'product': product})


def something(request):
    return render(request, 'ecomm/something.html', {'menu': menu, 'title': 'Что то полезное'})

