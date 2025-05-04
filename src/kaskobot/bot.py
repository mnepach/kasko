# -*- coding: utf-8 -*-

import res.messages as msg
import rates as rates
import calculations as calc

def get_vehicle_year():
    vehicleYear = input (msg.VEHICLE_YEAR_PROMPT + ": \n")
    return int(vehicleYear)

def get_vehicle_price():
    vehiclePrice = input (msg.VEHICLE_PRICE_PROMPT + ": \n")
    return int(vehiclePrice)

curUser = rates.UserInfo()
vehicleYear = get_vehicle_year()
vehiclePrice = get_vehicle_price()
curUser.set_vehicle_info(vehicleYear, vehiclePrice)
curUser.set_rates_from_programs()
curUser.calc_summary_values()
print(curUser.total_for_program)