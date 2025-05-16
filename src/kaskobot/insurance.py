# -*- coding: utf-8 -*-

import res.values as values
import kaskobot.calculations as calc
import kaskobot.program as prg
from kaskobot.vehicle import Vehicle
       
class Insurance:

    vehicle_data = Vehicle
    rates_from_programs = []
    totals_for_programs = []
    rb_only = True
    drivers = []

    def __init__(self):
        pass
        
    def set_vehicle_info(self, vehicle):
        self.vehicle_data = vehicle

    def set_drivers_info(self, drivers):
        self.drivers = drivers
    
    def set_rb_only(self, rb_only_indicator):
        self.rb_only = rb_only_indicator

    def get_territory_rate(self):
        if (self.rb_only):
            _territory_rate = values.TERRITORY_RB_ONLY
        else:
            _territory_rate = values.TERRITORY_ALL
        return float(_territory_rate)
        
    def set_rates_from_programs(self):
        _all_programs = prg.AVAILABLE_PROGRAMS
        for i in _all_programs:
            _vehicle_year = self.vehicle_data.year_of_prod
            _vehicle_price = self.vehicle_data.price
            _rate_from_program = i.get_rate_from_program(_vehicle_year, 
                                                         _vehicle_price)
            self.rates_from_programs.append(_rate_from_program)

    def calc_summary_values(self):
        _base = values.BASE_VALUE
        _territory_rate = self.get_territory_rate()
        for i in range(0, len(self.rates_from_programs)):
            _rate = self.rates_from_programs[i]
            _total_for_program = _base * _rate * _territory_rate
            self.totals_for_programs.append(_total_for_program)
    

