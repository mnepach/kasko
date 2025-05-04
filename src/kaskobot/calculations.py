# -*- coding: utf-8 -*-

from datetime import date
from res import values as prg

def define_vehicle_age(vehYear):
    _curYear = date.today().year
    _vehicleAge = int(_curYear) - vehYear
    return str(_vehicleAge)

def define_price_index(vehPrice):
   
    _vehPriceIndex = 0
    _PRICE_LIMIT_1 = int(prg.VEHICLE_PRICE_LIMIT_1)
    _PRICE_LIMIT_2 = int(prg.VEHICLE_PRICE_LIMIT_2)
    _PRICE_LIMIT_3 = int(prg.VEHICLE_PRICE_LIMIT_3)

    if ((vehPrice >= 0) and (vehPrice <= _PRICE_LIMIT_1)):
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

'''
def calc_summary_value(user_rates):
    _base = prg.BASE_VALUE
    _summary_value = _base*user_rates
    return float(_summary_value)
'''