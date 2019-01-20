#!/usr/bin/python3

from flask import make_response, abort

import shop
from Item_Shop_classes import Cart

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
        abort(406, "There's no shopping cart open!")

    try:
        item = shop.MY_SHOP.get(itemname)
        my_cart.add(item)
    except ValueError:
        abort(406, "Can't add more than the available quantity!")
    except KeyError:
        abort(404, "The requested item doesn't exist in the shop!")
    return make_response("Added {} to the shopping cart".format(itemname), 200)


def view_cart():
    """
    Produce the contents of the Cart and its price total. Get a 406 if there's no Cart open.

    :return: A dict containing a price total and a list of dicts representing items in Cart.
        {
            'total' : Decimal,
            'items' : [
                {'product' : Item.dict(), 'quantity' : int}
            ]
        }
    :raise: werkzeug.exceptions.NotAcceptable
    """
    if my_cart is None:
        abort(406, "There's no shopping cart open!")

    return my_cart.view()


def close_cart():
    """
    Close the Cart. Get a 406 if it's not even open.

    :return: 200 OK
    :raise: werkzeug.exceptions.NotAcceptable
    """
    global my_cart
    if my_cart is None:
        abort(406, "The shopping cart is already closed!")

    del my_cart
    my_cart = None

    return make_response("Deleted the shopping cart", 200)


def remove_from_cart(itemname):
    """
    Reduce the quantity of the named item in Cart by 1. Get a 404 if the item doesn't
    exist in the shop. Get a 406 if the item isn't in the Cart or the Cart's not open.

    :param itemname: The item to look for and reduce quantity by 1.
    :type itemname: str
    :return: 200 OK
    :raise: werkzeug.exceptions.NotFound
            werkzeug.exceptions.NotAcceptable
    """
    if my_cart is None:
        abort(406, "There's no shopping cart open!")

    try:
        shop.MY_SHOP.get(itemname)
        my_cart.remove(itemname)
    except KeyError:
        abort(404, "The requested item doesn't exist in the shop!")
    except NameError:
        abort(406, "The requested item isn't in the shopping cart!")
    return make_response("Removed 1 {} from the shopping cart".format(itemname), 200)


def checkout_cart():
    """
    Check that each item in the Cart isn't exceeding available stock in the Shop. If so,
    buy every item from the shop at the requested quantities, then close the cart.
    Otherwise, get a 406 if the Cart contains too many of an item or the Cart's not open.

    :return: 200 OK
    :raise: werkzeug.exceptions.NotAcceptable
    """
    global my_cart

    if my_cart is None:
        abort(406, "There's no shopping cart open!")

    for i in my_cart.items:
        itemname = i['product'].title
        shopitem = shop.MY_SHOP.get(itemname)
        if i['quantity'] > shopitem.inventory_count:
            abort(406, "Not enough items in stock to fulfill cart checkout!")

    for i in my_cart.items:
        for _ in range(i['quantity']):
            shop.buy(i['product'].title)

    checkout_total = my_cart.total
    del my_cart
    my_cart = None
    return make_response("Checkout complete: ${} purchased.".format(checkout_total), 200)
