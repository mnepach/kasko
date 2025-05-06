# -*- coding: utf-8 -*-

from datetime import date
from res import values as values

def define_age(year):
    _curYear = date.today().year
    _age = int(_curYear) - year
    return _age

