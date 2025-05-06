# -*- coding: utf-8 -*-

import res.values as values
import kaskobot.calculations as calc
import kaskobot.program as prg

class Insurance:
    vehicle_data = {
        'year': 0,
        'price': 0
    }
    meta_data = {
        'year_index': 0,
        'price_index': 0
        }
    rates_from_programs = []
    totals_for_programs = []

    def __init__(self):
        pass
        
    def set_vehicle_info(self, year, price):
        self.vehicle_data['year'] = year
        self.vehicle_data['price'] = price
        self.meta_data['year_index'] = str(calc.define_age(year))
        self.meta_data['price_index'] = calc.define_price_index(price)
        self.year_index = str(calc.define_age(year))
        self.price_index = calc.define_price_index(price)
         
    def set_rates_from_programs(self):
        _all_programs = prg.AVAILABLE_PROGRAMS
        for i in _all_programs:
            _rate_from_program =\
                  i._program_rates_a\
                    [self.meta_data['year_index']]\
                        [self.meta_data['price_index']]
            self.rates_from_programs.append(_rate_from_program)

    def calc_summary_values(self):
        _base = values.BASE_VALUE
        for i in range(0, len(self.rates_from_programs)):
            _rate = self.rates_from_programs[i]
            _total_for_program = _base * _rate
            self.totals_for_programs.append(_total_for_program)
    

