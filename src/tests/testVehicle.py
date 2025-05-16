# -*- encoding: utf-8 -*

import unittest
import res.values as values
from kaskobot.vehicle import Vehicle

class TestDriver(unittest.TestCase):
    def setUp(self):
        self.vehTstObj = Vehicle()
        return super().setUp()
    
    def test_set_vehicle_production_year(self):
        _test_data = 2024
        self.vehTstObj.set_vehicle_production_year(_test_data)
        self.assertEqual(self.vehTstObj.year_of_prod, _test_data)

    def test_set_vehicle_price(self):
        _test_data = 14236
        self.vehTstObj.set_vehicle_price(_test_data)
        self.assertEqual(self.vehTstObj.price, _test_data)

    def test_set_is_geely_true(self):
        self.vehTstObj.set_is_geely(True)
        self.assertTrue(self.vehTstObj.is_geely)

    def test_set_is_geely_false(self):
        self.vehTstObj.set_is_geely(False)
        self.assertFalse(self.vehTstObj.is_geely)

    def test_set_is_bmw_true(self):
        self.vehTstObj.set_is_bmw(True)
        self.assertTrue(self.vehTstObj.is_bmw)

    def test_set_is_bmw_false(self):
        self.vehTstObj.set_is_bmw(False)
        self.assertFalse(self.vehTstObj.is_bmw)