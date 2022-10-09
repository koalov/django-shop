from django.shortcuts import render
from ecomm.models import *
from django.db import *


def filter_page(request):
    get_query = request.GET.get('query')
    get_product_type = request.GET.get('product_type')
    values = ProductSpecificationValue.objects.filter(value=get_query)

    correct_values = []

    for value in values:
        if value.product.category.name == get_product_type:
            correct_values.append(value)

    return render(request, 'filter/filter_list.html', context={'values': correct_values,
                                                               'filter_name': get_query})