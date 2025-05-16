# -*- coding: utf-8 -*-
import res.values as values
import kaskobot.calculations as calc

class Driver:
    age = 0
    expirience = 0
    rate = 0
    
    def __init__(self):
        pass

    def set_driver_age(self, age):
        self.age = age

    def set_driver_expirience(self, expirience):
        self.expirience = expirience
    
    def _define_expirience_row(self):
        if (self.expirience < 1):
            _exp_row_number = 0
        elif self.expirience < 2:
            _exp_row_number = 1
        else:
            _exp_row_number = 2
        return(_exp_row_number)
    
    def _define_age_column(self):
        _age_limits = [
              values.DRIVER_AGE_LIMIT_1,
              values.DRIVER_AGE_LIMIT_2,
              values.DRIVER_AGE_LIMIT_3
              ]
        for i in range(0, len(_age_limits)):
            if self.age >= _age_limits[i]:
                _age_column_number = i
        return(_age_column_number)

    def define_driver_rate(self):
        _rates_table = values.DRIVER_RATES
        _driver_rates = {}
        for i in range(0, len(_rates_table)):
            _driver_rates[str(i)] = _rates_table[i]
        _exp_row_number = str(self._define_expirience_row())
        _age_column_number = self._define_age_column()
        self.rate = _driver_rates[_exp_row_number][_age_column_number]
