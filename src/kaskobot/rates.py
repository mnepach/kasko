# -*- coding: utf-8 -*-
import res.values as prg
import calculations as calc

class ProgramInfo:
    
    def __init__(self, list_a):
        self._program_name = ""
        self._program_rates_a = {}
        self._program_rates_b = {}
        for i in range(0, (len(list_a))):
            self._program_rates_a[str(i)] = list_a[i]
    
    def get_rate_from_program(program, year, price):
        _rate_from_program = program._program_rates_a[year][price]
        return float(_rate_from_program)

class UserInfo:
    vehicle_year = 0
    year_index = 0
    vehicle_price = 0
    price_index = 0
    program_name = ""
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
            _rate_from_program = i._program_rates_a[self.year_index][self.price_index]
            self.rate_from_program.append(_rate_from_program)
    
OPTIMA_A_RATES = ProgramInfo (prg.OPTIMA_A)
PROFIT_A_RATES = ProgramInfo (prg.PROFIT_A)
AVAILABLE_PROGRAMS = [
    OPTIMA_A_RATES, 
    PROFIT_A_RATES
    ]


