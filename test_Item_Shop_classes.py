#!/usr/bin/python3

from decimal import *
from Item_Shop_classes import Item, Shop
import pytest

DUMMY_ITEM = {
    'title': "Cup",
    'price': Decimal('1.00'),
    'inventory_count': 4
}

ITEM_LIST = [
    DUMMY_ITEM,
    {
        'title': "Fork",
        'price': Decimal('2.49'),
        'inventory_count': 10
    },
    {
        'title': "Ballpoint pens, 100 pack",
        'price': Decimal('12.99'),
        'inventory_count': 2
    }
]

ITEM_LIST_2 = [
    DUMMY_ITEM,
    {
        'title': "Arid Mesa",
        'price': Decimal('50.00'),
        'inventory_count': 0
    }
]


class TestItem:
    def test_init_item(self):
        cup = Item(DUMMY_ITEM)
        assert cup is not None
        assert cup.title == "Cup"
        assert cup.price == Decimal('1.00')
        assert cup.inventory_count == 4

    def test_negative_stock(self):
        cup = Item(DUMMY_ITEM)
        cup.inventory_count -= 1
        assert cup.inventory_count == 3
        with pytest.raises(ValueError):
            cup.inventory_count -= 99

    def test_item_equality(self):
        cup = Item(DUMMY_ITEM)
        assert cup == Item(DUMMY_ITEM)


class TestShop:
    def test_init_shop(self):
        s = Shop(ITEM_LIST)
        assert len(s) == 3
        assert s[0] == Item({
            'title': "Ballpoint pens, 100 pack",
            'price': Decimal('12.99'),
            'inventory_count': 2
        })
        assert s[1] == Item(DUMMY_ITEM)
        assert s[2] == Item({
            'title': "Fork",
            'price': Decimal('2.49'),
            'inventory_count': 10
        })

    def test_init_empty_shop(self):
        s = Shop([])
        assert len(s) == 0
        with pytest.raises(IndexError):
            x = s[0]

    def test_duplicate_titles(self):
        with pytest.raises(NameError):
            Shop([DUMMY_ITEM, DUMMY_ITEM])

    def test_get_item_by_name(self):
        s = Shop(ITEM_LIST)
        assert s.get('Fork') == Item({
            'title': "Fork",
            'price': Decimal('2.49'),
            'inventory_count': 10
        })
        with pytest.raises(KeyError):
            s.get('Antimatter')

    def test_list_of_dicts(self):
        s = Shop(ITEM_LIST)
        assert s.list_of_dicts() == [
            {
                'title': "Ballpoint pens, 100 pack",
                'price': Decimal('12.99'),
                'inventory_count': 2
            },
            {
                'title': "Cup",
                'price': Decimal('1.00'),
                'inventory_count': 4
            },
            {
                'title': "Fork",
                'price': Decimal('2.49'),
                'inventory_count': 10
            }
        ]

        s = Shop(ITEM_LIST_2)
        assert s.list_of_dicts(in_stock_only=True) == [DUMMY_ITEM]
