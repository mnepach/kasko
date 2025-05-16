# -*- encoding: utf-8 -*

import unittest
import res.values as values
from kaskobot.driver import Driver

class TestDriver(unittest.TestCase):
    def setUp(self):
        self.drvTstObj = Driver()
        return super().setUp()
    
    def test_set_driver_age(self):
        _test_data = 24
        self.drvTstObj.set_driver_age(_test_data)
        self.assertEqual(self.drvTstObj.age, _test_data)

    def test_set_driver_expirience(self):
        _test_data = 10
        self.drvTstObj.set_driver_expirience(_test_data)
        self.assertEqual(self.drvTstObj.expirience, _test_data)
    
    def test_define_age_culumn_number_0(self):
        _test_values = [16, 20, 24]
        for i in _test_values:
            with self.subTest(age=i):
                self.drvTstObj.age = i
                self.assertEqual(self.drvTstObj._define_age_column(), 0)

    def test_define_age_culumn_number_1(self):
        _test_values = [25, 30, 34]
        for i in _test_values:
            with self.subTest(age=i):
                self.drvTstObj.age = i
                self.assertEqual(self.drvTstObj._define_age_column(), 1)

    def test_define_age_culumn_number_2(self):
        _test_values = [35, 50, 100]
        for i in _test_values:
            with self.subTest(age=i):
                self.drvTstObj.age = i
                self.assertEqual(self.drvTstObj._define_age_column(), 2)

    def test_define_expirience_row_0(self):
        self.drvTstObj.expirience = 0
        self.assertEqual(self.drvTstObj._define_expirience_row(), 0)

    def test_define_expirience_row_1(self):
        self.drvTstObj.expirience = 1
        self.assertEqual(self.drvTstObj._define_expirience_row(), 1)

    def test_define_expirience_row_2(self):
        _test_values = [2, 10, 99]
        for i in _test_values:
            with self.subTest(expierence=i):
                self.drvTstObj.expirience = i
                self.assertEqual(self.drvTstObj._define_expirience_row(), 2)