# -*- encoding: utf-8 -*

import unittest
import res.values as values
from kaskobot.insurance import Insurance

class TestProgram(unittest.TestCase):
    def setUp(self):
        self.insTstObj = Insurance()
        return super().setUp()
    
    def test_set_rb_only_true(self):
        self.insTstObj.set_rb_only(True)
        self.assertTrue(self.insTstObj.rb_only)

    def test_set_rb_only_false(self):
        self.insTstObj.set_rb_only(False)
        self.assertFalse(self.insTstObj.rb_only)

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
