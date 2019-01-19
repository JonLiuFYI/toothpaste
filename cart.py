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


def add_to_cart(itemname):
    """
    Add the named item to the Cart. Get a 404 if the item doesn't exist.
    Get a 406 if adding the item would go over available inventory.

    :param itemname: The item to look for and add
    :type itemname: str
    :return: 200 OK
    :raise: werkzeug.exceptions.NotFound
            werkzeug.exceptions.NotAcceptable
    """
    if my_cart is None:
        abort(406, "The shopping cart hasn't been created yet!")

    try:
        item = shop.MY_SHOP.get(itemname)
        my_cart.add(item)
    except ValueError:
        abort(406, "Can't add more than the available quantity!")
    except KeyError:
        abort(404, "The requested item doesn't exist in the shop!")
    return make_response("Added {} to the shopping cart".format(itemname), 200)


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

