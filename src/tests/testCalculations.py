# -*- encoding: utf-8 -*

import unittest
import kaskobot.calculations as calc

class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.calcTstObj = calc
        return super().setUp()
    
    def test_define_price_index(self):
        self.assertEqual(self.calcTstObj.define_price_index(14999), 0)