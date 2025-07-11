# -*- coding: utf-8 -*-

from ..res import values as values
from . import calculations as calc
from . import program as prg
from .vehicle import Vehicle 

class Insurance:

    vehicle_data = Vehicle() # Инициализируем объект Vehicle по умолчанию
    rates_from_programs = []
    totals_for_programs = {} # Изменено на словарь
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
        _all_programs = prg.AVAILABLE_PROGRAMS # Используем prg.AVAILABLE_PROGRAMS
        self.rates_from_programs = [] # Очищаем перед заполнением
        for i in _all_programs:
            _vehicle_year = self.vehicle_data.year_of_prod
            _vehicle_price = self.vehicle_data.price
            _rate_from_program = i.get_rate_from_program(_vehicle_year, 
                                                            _vehicle_price)
            self.rates_from_programs.append(_rate_from_program)

    def calc_summary_values(self):
        _base = values.BASE_VALUE
        _territory_rate = self.get_territory_rate()
        self.totals_for_programs = {} # Очищаем перед заполнением
        for i in range(0, len(self.rates_from_programs)):
            _rate = self.rates_from_programs[i]
            # Получаем имя программы
            if hasattr(prg.AVAILABLE_PROGRAMS[i], '_name') and prg.AVAILABLE_PROGRAMS[i]._name:
                _program_name = prg.AVAILABLE_PROGRAMS[i]._name
            else: # Если имя не установлено, попробуем по классу
                _program_name = prg.AVAILABLE_PROGRAMS[i].__class__.__name__ 

            _total_for_program = _base * _rate * _territory_rate
            self.totals_for_programs[_program_name] = _total_for_program