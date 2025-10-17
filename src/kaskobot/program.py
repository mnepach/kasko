from ..res import values
from . import calculations as calc

class BaseProgram:
    def __init__(self, name="", description="", rates=None):
        self._name = name
        self._description = description
        self._rates = rates
        self._price_limits = [
            values.VEHICLE_PRICE_LIMIT_1,
            values.VEHICLE_PRICE_LIMIT_2,
            values.VEHICLE_PRICE_LIMIT_3,
            values.VEHICLE_PRICE_LIMIT_4
        ]

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_rate(self, vehicle_year, vehicle_price):
        if not self._rates:
            raise ValueError(f"Для программы {self._name} тарифы не заданы.")

        age_key = self._define_vehicle_age_key(vehicle_year)
        price_key = self._define_price_key(vehicle_price)
        return self._rates.get(age_key, {}).get(price_key)

    def get_min_premium(self, **kwargs):
        return values.MIN_PREMIUMS_PASSENGER.get(self._name)

    def _define_vehicle_age_key(self, vehicle_year):
        age_in_years, _ = calc.define_age(manufacture_year=vehicle_year)
        if age_in_years == 0: return "до года"
        elif age_in_years == 1: return "1 год"
        elif age_in_years == 2: return "2 года"
        elif age_in_years == 3: return "3 года"
        elif age_in_years == 4: return "4 года"
        elif age_in_years == 5: return "5 лет"
        elif age_in_years == 6: return "6 лет"
        else: return "7 лет"

    def _define_price_key(self, vehicle_price):
        for limit in self._price_limits:
            if vehicle_price <= limit:
                return limit
        return self._price_limits[-1]

class OptimaProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Оптима",
            description="Полное КАСКО без франшизы. Оплата без учета износа.",
            rates=values.OPTIMA_A_RATES
        )

class ProfitProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Профит",
            description="Полное КАСКО без франшизы, с особыми условиями по обращениям без документов.",
            rates=values.PROFIT_A_RATES
        )

class PremiumKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Премиум",
            description="Расширенное покрытие с дополнительными услугами.",
            rates=values.OPTIMA_A_RATES
        )

    def get_rate(self, vehicle_year, vehicle_price):
        base_rate = super().get_rate(vehicle_year, vehicle_price)
        return base_rate * values.PREMIUM_COEFF_BASE

    def get_min_premium(self, **kwargs):
        return values.MIN_PREMIUMS_PASSENGER["КАСКО-Премиум"]

AVAILABLE_PROGRAMS = {
    "КАСКО-Оптима": OptimaProgram(),
    "КАСКО-Профит": ProfitProgram(),
    "КАСКО-Премиум": PremiumKaskoProgram(),
}