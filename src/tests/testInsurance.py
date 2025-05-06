# -*- encoding: utf-8 -*

import unittest
import res.values as values
from kaskobot.insurance import Insurance

class TestProgram(unittest.TestCase):
    def setUp(self):
        self.insTstObj = Insurance()
        return super().setUp()
    
    def test_set_vehicle_info(self):
        _year = 2024
        _price = 14236
        self.insTstObj.set_vehicle_info(_year, _price)
        with self.subTest(year=_year):
            self.assertEqual(self.insTstObj.vehicle_data['year'], _year)
        with self.subTest(price=_price):
            self.assertEqual(self.insTstObj.vehicle_data['price'], _price)

    def test_set_territory_rate_rb_only(self):
        _rb_only = True
        _expected = values.TERRITORY_RB_ONLY
        self.insTstObj.set_territory_rate(_rb_only)
        self.assertEqual(self.insTstObj.territory_rate, _expected)

    def test_set_territory_rate_all(self):
        _rb_only = False
        _expected = values.TERRITORY_ALL
        self.insTstObj.set_territory_rate(_rb_only)
        self.assertEqual(self.insTstObj.territory_rate, _expected)