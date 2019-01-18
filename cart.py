#!/usr/bin/python3

from decimal import *
from flask import make_response, abort
from Item_Shop_classes import Shop, Item, Cart
import shop

my_cart = None


def create():
    """
    Create a Cart, then keep track of it in until the purchase is complete. There
    can only be one Cart open at once.

    :return: 201 Created
    :raise: werkzeug.exceptions.NotAcceptable
    """
    global my_cart
    if my_cart is not None:
        abort(406, "There's already a cart!")
    my_cart = Cart()
    return make_response("Opened a shopping cart", 201)


def add(itemname):
    """
    Add the named item to the Cart. Get a 404 if the item doesn't exist.
    Get a 406 if adding the item would go over available inventory.

    :param itemname: The item to look for and add
    :type itemname: str
    :return: 200 OK
    :raise: werkzeug.exceptions.NotFound
            werkzeug.exceptions.NotAcceptable
    """
    item = shop.MY_SHOP.get(itemname)
    try:
        my_cart.add(item)
    except ValueError:
        abort(406, "Can't add more than the available quantity!")

# TODO: finish view after adding
def view():
    """
    Produce the contents of the Cart. Get a 404 if there's no Cart open.

    :return: A list of dicts {product, quantity}. product is a dict {title, price,
    inventory_count} and quantity is an int.
    [
        {
        'product':
            {
            'title': str,
            'price': Decimal,
            'inventory_count': int
            },
        'quantity': int
        }
    ]
    """

