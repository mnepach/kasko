# -*- coding: utf-8 -*-
import kaskobot.res.values as prg

class ProgramRates:
    
    def __init__(self, list):

        self._program_rates_table = {
            '0': list[0],
            '1': list[1]
            }
    
    def get_rate_from_program(program, year, price):
        _rate_from_program = program._program_rates_table[year][price]
        return float(_rate_from_program)
    
OPTIMA_RATES = ProgramRates (prg.OPTIMA_A)

class UserRates:
    def __init_(self):
        self.user_rates = {
            'rate_from_program': 0.0
        }
