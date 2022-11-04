from .models import *

menu = [{'title': "About", 'url_name': 'about'},
        {'title': "Feedback", 'url_name': 'feedback'},
        {'title': "Something else", 'url_name': 'something'},
        {'title': "Cart", 'url_name': 'cart'},
        ]


def get_category_tree(request):
    category = Category.objects.filter(parent=None)
    category_tree = category.get_descendants(include_self=True)
    return {'category_tree': category_tree}
