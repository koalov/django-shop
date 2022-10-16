from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'feedback'},
        {'title': "Что-то ещё", 'url_name': 'something'},
        {'title': "Корзина", 'url_name': 'cart'},
        ]


def get_category_tree(request):
    category = Category.objects.filter(parent=None)
    category_tree = category.get_descendants(include_self=True)
    return {'category_tree': category_tree}
