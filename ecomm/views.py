# from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductSpecificationValue, ProductSpecification
from cart.form import CartAddProductForm
from shop.settings import GOOGLE_MAPS_API_KEY

# from django.views.generic import DetailView, ListView


def homepage(request):
    products = Product.objects.filter(available=True)
    context = {"products": products, "title": "Main page"}

    return render(request, "ecomm/main.html", context=context)


def category_page(request, slug):
    category = Category.objects.get(slug=slug)

    if category.level == 0:
        child_cat = category.children.all()
        context = {"category": category, "child_cat": child_cat}
        return render(request, "ecomm/category_parent.html", context=context)

    else:
        products = category.product_set.all()
        context = {"products": products, "category": category}

        sort = request.GET.get("sort")
        if sort:
            products = category.product_set.all()[: int(sort)]
            context["products"] = products

        return render(request, "ecomm/category_children.html", context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    product_spec = ProductSpecification.objects.all()
    product_spec_val = ProductSpecificationValue.objects.all()
    cart_product_form = CartAddProductForm()
    context = {
        "product_spec": product_spec,
        "product_spec_val": product_spec_val,
        "product": product,
        "cart_product_form": cart_product_form,
    }

    return render(request, "ecomm/product.html", context=context)


def feedback(request):
    return render(
        request,
        "ecomm/feedback.html",
        {"title": "Feedback", "myapi": GOOGLE_MAPS_API_KEY},
    )


def something(request):
    return render(request, "ecomm/policy.html", {"title": "Something useful"})


def about(request):
    return render(request, "ecomm/about.html", {"title": "About"})
