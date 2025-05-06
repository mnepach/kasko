# -*- encoding: utf-8 -*

import unittest
import res.values as values
import kaskobot.program as prg

class TestProgram(unittest.TestCase):
    def setUp(self):
        self.prgTstObj = prg.Program(values.OPTIMA_A)
        return super().setUp()
    
    def test_define_price_culumn_number_0(self):
        _test_values = [1, 10000, 14999, 15000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.prgTstObj.define_price_column_number(i), 0)

    def test_define_price_culumn_number_1(self):
        _test_values = [15001, 20000, 29999, 30000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.prgTstObj.define_price_column_number(i), 1)

    def test_define_price_culumn_number_2(self):
        _test_values = [30001, 40000, 49999, 50000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.prgTstObj.define_price_column_number(i), 2)

    def test_define_price_culumn_number_3(self):
        _test_values = [50001, 60000, 10000000]
        for i in _test_values:
            with self.subTest(price=i):
                self.assertEqual(self.prgTstObj.define_price_column_number(i), 3)