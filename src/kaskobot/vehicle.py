# -*- coding: utf-8 -*-

class Vehicle:
    year_of_prod = 0
    price = 0
    is_geely = False
    is_bmw = False
    
    def __init__(self):
        pass

    def set_vehicle_production_year(self, year):
        self.year_of_prod = year

    def set_vehicle_price(self, price):
        self.price = price

    def set_is_geely(self, is_geely_indicator):
        self.is_geely = is_geely_indicator

    def set_is_bmw(self, is_bmw_indicator):
        self.is_bmw = is_bmw_indicator