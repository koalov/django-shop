from collections import UserDict
from decimal import Decimal
from django.conf import settings
from ecomm.models import Product


class CartLogic:

    def __init__(self, request, *args, **kwargs):
        """
        Cart initialization
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to the cart or updating its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        self.session['counter_items'] = self.counter()

    def save(self):
        # Updating cart session
        self.session[settings.CART_SESSION_ID] = self.cart
        # Marked session as "changed" for ensure that product is saved
        self.session.modified = True

    def remove(self, product):
        """
        Deleting product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session['counter_items'] = self.counter()
            self.save()

    def __iter__(self):
        """
        Selection products in the cart and receiving them from database.
        """
        product_ids = self.cart.keys()
        # receiving product objects and adding them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Counting total products in the cart.
        """
        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price(self):
        """
        Counting of total price in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session['counter_items'] = self.counter()
        self.session.modified = True

    def counter(self):
        """Returns quantity of the products in the cart"""
        counter = 0
        for item in self.cart.values():
            counter += item.get('quantity', 0)
        return counter
