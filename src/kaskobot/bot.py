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

vehicleYear = get_vehicle_year()
vehiclePrice = get_vehicle_price()
yearIndex = calc.define_vehicle_age(vehicleYear)
priceIndex=calc.define_price_index(vehiclePrice)
#optima = rates.ProgramRates()
#print(rates.OPTIMA.program_rates_table)
user_rate = rates.ProgramRates.get_rate_from_program(
    rates.OPTIMA_RATES,yearIndex,priceIndex
    )
print(calc.calc_summary_value(user_rate))