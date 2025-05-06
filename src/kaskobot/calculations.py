# -*- coding: utf-8 -*-

from datetime import date
from res import values as values

def define_age(year):
    _curYear = date.today().year
    _age = int(_curYear) - year
    return _age

def define_price_index(vehPrice):
   
    _vehPriceIndex = 0
    _PRICE_LIMIT_1 = int(values.VEHICLE_PRICE_LIMIT_1)
    _PRICE_LIMIT_2 = int(values.VEHICLE_PRICE_LIMIT_2)
    _PRICE_LIMIT_3 = int(values.VEHICLE_PRICE_LIMIT_3)

    if ((vehPrice > 0) and (vehPrice <= _PRICE_LIMIT_1)):
        _vehPriceIndex = 0
    elif ((vehPrice > _PRICE_LIMIT_1) and (vehPrice <= _PRICE_LIMIT_2)):
        _vehPriceIndex = 1
    elif ((vehPrice > _PRICE_LIMIT_2) and (vehPrice <= _PRICE_LIMIT_3)):
        _vehPriceIndex = 2
    elif (vehPrice > _PRICE_LIMIT_3):
        _vehPriceIndex = 3
    else:
        _vehPriceIndex = -1
    return int(_vehPriceIndex)
