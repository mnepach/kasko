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
    _rb_only = answer_to_bool(_answer)
    return (_rb_only)

def get_geely_info():
    _answer = input (msg.IS_GEELY_PROMPT + ": ")
    _is_geely = answer_to_bool(_answer)
    return (_is_geely)

def get_bmw_info():
    _answer = input (msg.IS_BMW_PROMPT + ": ")
    _is_bmw = answer_to_bool(_answer)
    return (_is_bmw)

def answer_to_bool(answer):
    answer.upper()
    if (answer == 'Y'):
        _response = True
    elif (answer == 'N'):
        _response = False
    return (_response)


def run_bot():
    curInsurance = Insurance()
    vehicle_production_year = get_vehicle_year()
    vehicle_price = get_vehicle_price()
    #territory_ind = get_territory_info()
    #geely_ind = get_geely_info()
    #bmw_ind = get_bmw_info()
    curInsurance.set_vehicle_production_year(vehicle_production_year)
    curInsurance.set_vehicle_price(vehicle_price)
    #curInsurance.set_rb_only(territory_ind)
    #curInsurance.set_is_geely(geely_ind)
    #curInsurance.set_is_bmw(bmw_ind)
    curInsurance.set_rates_from_programs()
    curInsurance.calc_summary_values()
    print(curInsurance.totals_for_programs)

