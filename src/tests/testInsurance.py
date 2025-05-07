# -*- encoding: utf-8 -*

import unittest
import res.values as values
from kaskobot.insurance import Insurance

class TestProgram(unittest.TestCase):
    def setUp(self):
        self.insTstObj = Insurance()
        return super().setUp()
    
    def test_set_vehicle_production_year(self):
        _test_data = 2024
        _expected = 2024
        self.insTstObj.set_vehicle_production_year(_test_data)
        self.assertEqual(self.insTstObj.vehicle_data['prod_year'], _expected)

    def test_set_vehicle_price(self):
        _test_data = 14236
        _expected = 14236
        self.insTstObj.set_vehicle_price(_test_data)
        self.assertEqual(self.insTstObj.vehicle_data['price'], _expected)

    def test_set_rb_only_true(self):
        self.insTstObj.set_rb_only(True)
        self.assertTrue(self.insTstObj.rb_only)

    def test_set_rb_only_false(self):
        self.insTstObj.set_rb_only(False)
        self.assertFalse(self.insTstObj.rb_only)

    def test_set_is_geely_true(self):
        self.insTstObj.set_is_geely(True)
        self.assertTrue(self.insTstObj.vehicle_data['is_geely'])

    def test_set_is_geely_false(self):
        self.insTstObj.set_is_geely(False)
        self.assertFalse(self.insTstObj.vehicle_data['is_geely'])

    def test_set_is_bmw_true(self):
        self.insTstObj.set_is_bmw(True)
        self.assertTrue(self.insTstObj.vehicle_data['is_bmw'])

    def test_set_is_bmw_false(self):
        self.insTstObj.set_is_bmw(False)
        self.assertFalse(self.insTstObj.vehicle_data['is_bmw'])

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
