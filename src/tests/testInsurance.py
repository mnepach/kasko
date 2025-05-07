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

    def test_set_rb_only_true(self):
        _expected = True
        self.insTstObj.set_rb_only(True)
        self.assertEqual(self.insTstObj.rb_only, _expected)

    def test_set_rb_only_false(self):
        _expected = False
        self.insTstObj.set_rb_only(False)
        self.assertEqual(self.insTstObj.rb_only, _expected)

    def test_get_territory_rate_rb_only(self):
        self.insTstObj.rb_only = True
        _expected = values.TERRITORY_RB_ONLY
        _rate = self.insTstObj.get_territory_rate()
        self.assertEqual(_rate, _expected)

    def test_get_territory_rate_all(self):
        self.insTstObj.rb_only = False
        _expected = values.TERRITORY_ALL
        _rate = self.insTstObj.get_territory_rate()
        self.assertEqual(_rate, _expected)
