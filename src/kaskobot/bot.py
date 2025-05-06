# -*- coding: utf-8 -*-

from res import messages as msg
import kaskobot.insurance as insurance

def get_vehicle_year():
    vehicleYear = input (msg.VEHICLE_YEAR_PROMPT + ": \n")
    return int(vehicleYear)

def get_vehicle_price():
    vehiclePrice = input (msg.VEHICLE_PRICE_PROMPT + ": \n")
    return int(vehiclePrice)

def run_bot():
    curInsurance = insurance.Insurance()
    vehicleYear = get_vehicle_year()
    vehiclePrice = get_vehicle_price()
    curInsurance.set_vehicle_info(vehicleYear, vehiclePrice)
    curInsurance.set_rates_from_programs()
    curInsurance.calc_summary_values()
    print(curInsurance.totals_for_programs)

