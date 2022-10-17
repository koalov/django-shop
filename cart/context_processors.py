from .cart import CartLogic


def cart(request):
    return {'cart': CartLogic(request)}
