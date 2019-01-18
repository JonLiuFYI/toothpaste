#!/usr/bin/python3

from decimal import *


class Item:
    """
    A product in the shop. Constructed with a dict containing the data.
    {
        title : str
        price : Decimal
        inventory_count : int
    }
    """

    def __init__(self, i):
        self.title = i['title']
        self.price = i['price']
        self._inventory_count = i['inventory_count']

    @property
    def inventory_count(self):
        return self._inventory_count

    @inventory_count.setter
    def inventory_count(self, n):
        if n < 0:
            raise ValueError("inventory_count can't be reduced to below 0")
        self._inventory_count = n

    def dict(self):
        """
        Produce a dict of this Item with matching keys and values.

        :return: dict. self with fields as dict keys.
        """
        return {
            'title': self.title,
            'price': self.price,
            'inventory_count': self._inventory_count
        }

    def __eq__(self, other):
        if isinstance(other, Item):
            return (self.title == other.title
                    and self.price == other.price
                    and self.inventory_count == other.inventory_count)
        elif isinstance(other, dict):
            return (self.title == other['title']
                    and self.price == other['price']
                    and self.inventory_count == other['inventory_count'])
        return False


class Shop:
    """
    Collection of all Items on sale, sorted by title. Constructed with a list of
    dicts containing item data. Duplicate named items aren't allowed.
    [
        {
            title : str
            price : Decimal
            inventory_count : int
        }
    ]
    """

    def __init__(self, itemlist):
        self.items = []
        self.names = []
        for i in sorted(itemlist, key=lambda j: j['title']):
            if i['title'] in self.names:
                raise NameError("There's already an item with that name")
            self.items.append(Item(i))
            self.names.append(i['title'])

    def get(self, itemname):
        """
        Find and return the item in this Shop with itemname as title.

        :param itemname: title to look for
        :type itemname: str
        :return: Item
        :raise: KeyError
        """
        if itemname not in self.names:
            raise KeyError
        return [i for i in self.items if i.title == itemname][0]

    def list_of_dicts(self, in_stock_only=False):
        """
        Produce a list, sorted by Item title, of every Item converted to a dict. If
        in_stock_only is True, exclude all Items with inventory_count 0.

        :param in_stock_only: Should the list contain only items that are in stock?
        :type in_stock_only: bool
        :return: List of dict. A list of Items converted to dicts, sorted by title.
        """
        return [i.dict() for i in self.items
                if (i.inventory_count > 0 if in_stock_only else True)]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        return self.items[n]


class Cart:
    """
    Collection of Items that a user wants to buy. Internally stored as a list of dicts
    {product, quantity}.
    [{'product' : Item, 'quantity' : int}]
    """

    def __init__(self):
        self.items = []
        self.names = []
        self.total = Decimal(0)

    def add(self, item):
        """
        Add the given item to the Cart. If it's already in the cart, increase the
        quantity to be purchased unless that would go over inventory_count.

        :param item: The item to add
        :type item: Item
        :return: None
        :raise: ValueError
        """
        if item.title in self.names:
            if self.items[self.names.index(item.title)]['quantity'] == item.inventory_count:
                raise ValueError("Can't add more than there's available")
            self.items[self.names.index(item.title)]['quantity'] += 1
        else:
            self.names.append(item.title)
            self.items.append({'product': item, 'quantity': 1})
        self.total += item.price

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        return self.items[n]
