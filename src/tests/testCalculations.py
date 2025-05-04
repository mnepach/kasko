# -*- encoding: utf-8 -*

import unittest
import kaskobot.calculations as calc

class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.calcTstObj = calc
        return super().setUp()
    
    def test_define_price_index_0(self):
        _test_values = [1, 10000, 14999, 15000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.calcTstObj.define_price_index(i), 0)

    def test_define_price_index_1(self):
        _test_values = [15001, 20000, 29999, 30000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.calcTstObj.define_price_index(i), 1)

    def test_define_price_index_2(self):
        _test_values = [30001, 40000, 49999, 50000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.calcTstObj.define_price_index(i), 2)

    def test_define_price_index_3(self):
        _test_values = [50001, 60000, 10000000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.calcTstObj.define_price_index(i), 3)