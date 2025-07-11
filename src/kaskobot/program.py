# -*- coding: utf-8 -*-

from ..res import values as values
from . import calculations as calc

class Program:
    _name = "" 
    _price_limits = [
        values.VEHICLE_PRICE_LIMIT_1,
        values.VEHICLE_PRICE_LIMIT_2,
        values.VEHICLE_PRICE_LIMIT_3
    ]

    def __init__(self, list_a, name=""): 
        self._rates_a = {}
        for i in range(0, len(list_a)):
            self._rates_a[str(i)] = list_a[i]
        self._name = name 

    def get_rate_from_program(self, year, price):
        _row_number = self.define_vehicle_age_row_number(year)
        _column_number = self.define_price_column_number(price)
        _rate = self._rates_a[_row_number][_column_number]
        return float(_rate)

    def define_vehicle_age_row_number(self, vehicle_year):
        _age_row_number = calc.define_age(vehicle_year)
        #  логика для обработки возраста выходящего за пределы таблицы
        if _age_row_number >= len(self._rates_a):
            _age_row_number = len(self._rates_a) - 1 
        return str(_age_row_number)

    def define_price_column_number(self, vehihcle_price):
        _price_column_number = 0
        if (vehihcle_price > 0 ):
            for i in range(0, len(self._price_limits)):
                if vehihcle_price > self._price_limits[i]:
                    _price_column_number = i + 1
        # логика для обработки цены выходящей за пределы таблицы
        if _price_column_number >= len(list(self._rates_a.values())[0]):
            _price_column_number = len(list(self._rates_a.values())[0]) - 1
        return int(_price_column_number)

OPTIMA = Program(values.OPTIMA_A_RATES, "OPTIMA")
PROFIT = Program(values.PROFIT_A_RATES, "PROFIT")

AVAILABLE_PROGRAMS = [
    OPTIMA, 
    PROFIT
]