# -*- coding: utf-8 -*-

from res import messages as msg
from kaskobot.insurance import Insurance
from kaskobot.driver import Driver
from kaskobot.vehicle import Vehicle

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

def get_vehicle_info():
    _year = get_vehicle_year()
    _price = get_vehicle_price()
    _is_geely = get_geely_info()
    _is_bmw = get_bmw_info()
    _vehicle = Vehicle()
    _vehicle.set_vehicle_production_year(_year)
    _vehicle.set_vehicle_price(_price)
    _vehicle.set_is_geely(_is_geely)
    _vehicle.set_is_bmw(_is_bmw)
    return _vehicle

def answer_to_bool(answer):
    answer.upper()
    _response = False
    if (answer == 'Y'):
        _response = True
    return (_response)

def get_driver_age():
    _answer = input (msg.DRIVER_AGE_PROMPT + ": ")
    return (_answer)

def get_driver_expirience():
    _answer = input (msg.DRIVER_EXP_PROMPT + ": ")
    return (_answer)

def get_driver_info():
    _age = get_driver_age()
    _expirience = get_driver_expirience()
    _driver = Driver()
    _driver.set_driver_age(_age)
    _driver.set_driver_expirience(_expirience)
    return _driver

def get_drivers_info():
        _drivers_count = input (msg.DRIVER_COUNT_PROMPT + ": ")
        _drivers = []
        for i in range (int(_drivers_count)):
            _current_driver = get_driver_info()
            _drivers.append(_current_driver)
        return _drivers

def run_bot():
    curInsurance = Insurance()
    #vehicle_production_year = get_vehicle_year()
    #vehicle_price = get_vehicle_price()
    #territory_ind = get_territory_info()
    #geely_ind = get_geely_info()
    #bmw_ind = get_bmw_info()
    #curInsurance.set_vehicle_production_year(vehicle_production_year)
    #curInsurance.set_vehicle_price(vehicle_price)
    #curInsurance.set_rb_only(territory_ind)
    #curInsurance.set_is_geely(geely_ind)
    #curInsurance.set_is_bmw(bmw_ind)
    vehicle = get_vehicle_info()
    curInsurance.set_vehicle_info(vehicle)
    drivers = get_drivers_info()
    curInsurance.set_drivers_info(drivers)
    curInsurance.set_rates_from_programs()
    curInsurance.calc_summary_values()
    print(curInsurance.totals_for_programs)

