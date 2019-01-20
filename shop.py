#!/usr/bin/python3

from decimal import *
from flask import abort
from Item_Shop_classes import Shop

# this would be from a database
fake_db = [
    {
        'title': "French hen",
        'price': Decimal('10.17'),
        'inventory_count': 3
    },
    {
        'title': "Turtle dove",
        'price': Decimal('12.25'),
        'inventory_count': 2
    },
    {
        'title': "Partridge in a pear tree",
        'price': Decimal('9.99'),
        'inventory_count': 1
    },
    {
        'title': "Chachalaca",
        'price': Decimal('3.50'),
        'inventory_count': 0
    }
]

# may be changed externally to set up for unit tests
MY_SHOP = Shop(fake_db)


def list_items(in_stock_only=False):
    """
    GET a sorted list of every item in the shop. If in_stock_only is True, exclude
    items that are out of stock.

    :param in_stock_only: Should the list only contain items that are in stock?
    :type in_stock_only: bool
    :return: List of dicts. All products, sorted by title.
    """
    return MY_SHOP.list_of_dicts(in_stock_only)


def find_one_item(itemname):
    """
    GET the one item in the shop whose title matches itemname.

    :param itemname: The title to look for in the shop.
    :type itemname: str
    :return: dict(str, Decimal, int). A dict representing the requested item.
    :raise: werkzeug.exceptions.NotFound
    """
    try:
        return MY_SHOP.get(itemname).dict()
    except KeyError:
        abort(404, "There's no product named {}!".format(itemname))


def buy(itemname):
    """
    Find the item whose title matches itemname. If it's in stock, PUT the new
    inventory_count, reduced by 1.

    :param itemname: The title to look for in the shop, then buy.
    :type itemname: str
    :return: Decimal. The cost to be charged for the purchased item.
    :raise: werkzeug.exceptions.NotFound
            werkzeug.exceptions.NotAcceptable
    """
    try:
        item = MY_SHOP.get(itemname)
        item.inventory_count -= 1
        return item.price
    except KeyError:
        abort(404, "There's no product named {}!".format(itemname))
    except ValueError:
        abort(406, "{} is out of stock!".format(itemname))
