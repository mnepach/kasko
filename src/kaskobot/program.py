# -*- coding: utf-8 -*-

import res.values as values

class Program:
    program_name = ""
    
    def __init__(self, list_a):
        self._program_rates_a = {}
        self._program_rates_b = {}
        for i in range(0, len(list_a)):
            self._program_rates_a[str(i)] = list_a[i]

OPTIMA_A_RATES = Program(values.OPTIMA_A)
PROFIT_A_RATES = Program(values.PROFIT_A)

AVAILABLE_PROGRAMS = [
    OPTIMA_A_RATES, 
    PROFIT_A_RATES
    ]
