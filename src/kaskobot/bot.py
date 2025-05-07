# -*- coding: utf-8 -*-

from res import messages as msg
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
    vehicle_production_year = get_vehicle_year()
    vehicle_price = get_vehicle_price()
    territory_ind = get_territory_info()
    curInsurance.set_rb_only(territory_ind)
    curInsurance.set_vehicle_production_year(vehicle_production_year)
    curInsurance.set_vehicle_price(vehicle_price)
    curInsurance.set_rates_from_programs()
    curInsurance.calc_summary_values()
    print(curInsurance.totals_for_programs)

