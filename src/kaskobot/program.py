# -*- coding: utf-8 -*-

import res.values as values
import kaskobot.calculations as calc

class Program:
    program_name = ""
    program_price_limits = [
        values.VEHICLE_PRICE_LIMIT_1,
        values.VEHICLE_PRICE_LIMIT_2,
        values.VEHICLE_PRICE_LIMIT_3
    ]
    
    def __init__(self, list_a):
        self._program_rates_a = {}
        self._program_rates_b = {}
        for i in range(0, len(list_a)):
            self._program_rates_a[str(i)] = list_a[i]

    def get_rate_from_program(self, year, price):
        _row_number = self.define_vehicle_age_row_number(year)
        _column_number = self.define_price_column_number(price)
        _rate = self._program_rates_a[_row_number][_column_number]
        return float(_rate)
    
    def define_vehicle_age_row_number(self, vehicle_year):
        _age_row_number = calc.define_age(vehicle_year)
        return str(_age_row_number)
    
    def define_price_column_number(self, vehihcle_price):
        if (vehihcle_price > 0 ):
            _price_column_number = 0
            for i in range(0, len(self.program_price_limits)):
                 if vehihcle_price > self.program_price_limits[i]:
                    _price_column_number = i + 1
        return int(_price_column_number)

OPTIMA = Program(values.OPTIMA_A_RATES)
PROFIT = Program(values.PROFIT_A_RATES)

AVAILABLE_PROGRAMS = [
    OPTIMA, 
    PROFIT
    ]
