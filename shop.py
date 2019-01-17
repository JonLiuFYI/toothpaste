#!/usr/bin/python3

from decimal import *

# this would be in a database
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
ITEMS = fake_db


def list_items(in_stock_only=False):
    """
    GET a sorted list of every item in the shop. If in_stock_only is True, exclude
    items that are out of stock.

    :param in_stock_only: Should the list only contain items that are in stock?
    :type in_stock_only: bool
    :return: List of dicts. All products, sorted by title.
    """
    return sorted([k for k in ITEMS
                   if (k['inventory_count'] > 0 if in_stock_only else True)],
                  key=lambda i: i['title'])
