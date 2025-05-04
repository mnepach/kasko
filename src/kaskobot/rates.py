# -*- coding: utf-8 -*-
import res.values as prg
import calculations as calc

class ProgramRates:
    
    def __init__(self, list):

        self._program_rates_table = {
            '0': list[0],
            '1': list[1]
            }
    
    def get_rate_from_program(program, year, price):
        _rate_from_program = program._program_rates_table[year][price]
        return float(_rate_from_program)

class UserRates:
    vehicle_year = 0
    year_index = 0
    vehicle_price = 0
    price_index = 0
    rate_from_program = []

    def __init_(self):
        pass

    def set_vehicle_info(self, year, price):
         self.vehicle_year = year
         self.vehicle_price = price
         self.year_index = calc.define_vehicle_age(year)
         self.price_index = calc.define_price_index(price)
         
    def set_rates_from_programs(self):
        _all_programs = AVAILABLE_PROGRAMS
        for i in _all_programs:
            _rate_from_program = i._program_rates_table[self.year_index][self.price_index]
            self.rate_from_program.append(_rate_from_program)
    
OPTIMA_A_RATES = ProgramRates (prg.OPTIMA_A)
PROFIT_A_RATES = ProgramRates (prg.PROFIT_A)
AVAILABLE_PROGRAMS = [
    OPTIMA_A_RATES, 
    PROFIT_A_RATES
    ]


