# -*- coding: utf-8 -*-

from res import messages as msg
#import kaskobot.insurance as insurance
from kaskobot.insurance import Insurance

def get_vehicle_year():
    _vehicleYear = input (msg.VEHICLE_YEAR_PROMPT + ": ")
    return int(_vehicleYear)

def get_vehicle_price():
    _vehiclePrice = input (msg.VEHICLE_PRICE_PROMPT + ": ")
    return int(_vehiclePrice)

def get_territory_info():
    _answer = input (msg.TERRITORY_PROMPT + ": ")
    _answer.upper()
    if (_answer == 'Y'):
        _rb_only = True
    elif (_answer == 'N'):
        _rb_only = False
    return (_rb_only)

def run_bot():
    curInsurance = Insurance()
    vehicleYear = get_vehicle_year()
    vehiclePrice = get_vehicle_price()
    territory_ind = get_territory_info()
    #curInsurance.set_territory_rate(territory_info)
    curInsurance.set_rb_only(territory_ind)
    curInsurance.set_vehicle_info(vehicleYear, vehiclePrice)
    curInsurance.set_rates_from_programs()
    curInsurance.calc_summary_values()
    print(curInsurance.totals_for_programs)

