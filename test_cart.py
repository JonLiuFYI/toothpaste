#!/usr/bin/python3

from decimal import *
import cart
from Item_Shop_classes import Shop, Item, Cart
import pytest
from werkzeug.exceptions import NotFound, NotAcceptable
import flask

f = flask.Flask(__name__)

HEN = {
    'title': "French hen",
    'price': Decimal('10.17'),
    'inventory_count': 3
}

DOVE = {
    'title': "Turtle dove",
    'price': Decimal('12.25'),
    'inventory_count': 2
}

CHACHALACA = {
    'title': "Chachalaca",
    'price': Decimal('3.50'),
    'inventory_count': 0
}


class TestCart:
    def test_create_cart_for_user(self):
        with f.app_context():
            cart.my_cart = None
            cart.create()
            assert cart.my_cart is not None

            with pytest.raises(NotAcceptable):
                cart.create()

    def test_add(self):
        with f.app_context():
            cart.my_cart = None
            cart.create()
            cart.add('French hen')
            cart.add('French hen')
            cart.add('Turtle dove')
            assert cart.my_cart.items == [
                {'product': HEN, 'quantity': 2},
                {'product': DOVE, 'quantity': 1}
            ]

            cart.add('French hen')
            with pytest.raises(NotAcceptable):
                cart.add('French hen')

    # TODO
    # add fake item to cart
    # test item not found
