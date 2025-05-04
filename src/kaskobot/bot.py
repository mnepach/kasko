# -*- coding: utf-8 -*-

import res.messages as msg
import rates as rates
import calculations as calc

def get_vehicle_year():
    vehicleYear = input (msg.VEHICLE_YEAR_PROMPT + ": \n")
    return int(vehicleYear)

def get_vehicle_price():
    vehiclePrice = input ("Price \n")
    return int(vehiclePrice)

curUser = rates.UserRates()
vehicleYear = get_vehicle_year()
vehiclePrice = get_vehicle_price()
curUser.set_vehicle_info(vehicleYear, vehiclePrice)
curUser.set_rates_from_programs()
#yearIndex = calc.define_vehicle_age(vehicleYear)
#priceIndex=calc.define_price_index(vehiclePrice)
#optima = rates.ProgramRates()
#print(rates.OPTIMA.program_rates_table)
#user_rate = rates.ProgramRates.get_rate_from_program(
#    rates.OPTIMA_A_RATES, yearIndex, priceIndex
#    )
#rates.set_rates_for_user(curUser, yearIndex, priceIndex)
print(curUser.rate_from_program)