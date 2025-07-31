from ..res import values
from . import calculations as calc

class BaseProgram:
    def __init__(self, name="", description="", rates_a=None, rates_b=None):
        self._name = name
        self._description = description
        self._rates_a = rates_a
        self._rates_b = rates_b
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

    def get_rate(self, vehicle_year, vehicle_price, insurance_variant):
        rates_to_use = self._rates_a if insurance_variant == "А" else self._rates_b
        if not rates_to_use:
            raise ValueError(f"Для программы {self._name} и варианта {insurance_variant} тарифы не заданы.")

        age_key = self._define_vehicle_age_key(vehicle_year)
        price_key = self._define_price_key(vehicle_price)
        return rates_to_use.get(age_key, rates_to_use.get("all", {})).get(price_key)

    def get_min_premium(self, insurance_variant, **kwargs):
        if self._name in ["КАСКО-Оптима", "КАСКО-Профит", "КАСКО-Автопрофи", "КАСКО-За полцены"]:
            return values.MIN_PREMIUMS_PASSENGER[self._name][insurance_variant]
        elif self._name == "КАСКО-за треть цены":
            return values.MIN_PREMIUMS_PASSENGER[self._name]
        return 0.0

    def _define_vehicle_age_key(self, vehicle_year):
        age_in_years = calc.define_age(manufacture_year=vehicle_year)
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
            description="Полное КАСКО без франшизы. Оплата без учета износа (А) или с учетом (Б).",
            rates_a=values.OPTIMA_A_RATES,
            rates_b=values.OPTIMA_B_RATES
        )

class ProfitProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Профит",
            description="Полное КАСКО без франшизы, с особыми условиями по обращениям без документов.",
            rates_a=values.PROFIT_A_RATES,
            rates_b=values.PROFIT_B_RATES
        )

class AutoprofiProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Автопрофи",
            description="Полное КАСКО с франшизой 200$.",
            rates_a=values.AUTOPROFI_A_RATES,
            rates_b=values.AUTOPROFI_B_RATES
        )

class HalfPriceProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-За полцены",
            description="Полное КАСКО с франшизой 500$ (до 50k$) или 700$ (свыше 50k$).",
            rates_a=values.HALF_PRICE_A_RATES,
            rates_b=values.HALF_PRICE_B_RATES
        )

class ThirdPriceProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-за треть цены",
            description="Полное КАСКО с франшизой 1000$ (до 50k$) или 1500$ (свыше 50k$).",
            rates_a=values.THIRD_PRICE_A_RATES,
            rates_b=values.THIRD_PRICE_B_RATES
        )

class GoodKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="Доброе КАСКО",
            description="Страхование только от полной гибели и хищения. Только Вариант Б.",
            rates_b=values.GOOD_KASKO_RATES
        )
        self._price_limits = [
            values.VEHICLE_PRICE_LIMIT_2,
            values.VEHICLE_PRICE_LIMIT_5,
            values.VEHICLE_PRICE_LIMIT_6
        ]

    def get_rate(self, vehicle_year, vehicle_price, insurance_variant):
        if insurance_variant == "А":
            raise ValueError("Доброе КАСКО доступно только для Варианта Б.")
        price_key = self._define_price_key(vehicle_price)
        return values.GOOD_KASKO_RATES.get(price_key)

    def get_min_premium(self, insurance_variant, **kwargs):
        return values.MIN_PREMIUMS_PASSENGER["Доброе КАСКО"]

class TransitKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Транзит",
            description="Для ТС с транзитными номерами. Короткие сроки (1-30 дней).",
            rates_a=values.TRANSIT_A_RATES,
            rates_b=values.TRANSIT_B_RATES
        )

    def get_rate(self, vehicle_year, vehicle_price, insurance_variant, transit_term_days=None):
        base_rate = super().get_rate(vehicle_year, vehicle_price, insurance_variant)
        if transit_term_days is None:
            raise ValueError("Для КАСКО-Транзит необходим срок страхования.")
        coeff = values.SHORT_TERM_COEFFS.get(
            7 if transit_term_days <= 7 else
            14 if transit_term_days <= 14 else
            30
        )
        return base_rate * coeff

    def get_min_premium(self, insurance_variant, transit_term_days=None):
        if transit_term_days is None:
            return 0.0
        return values.MIN_PREMIUMS_PASSENGER["КАСКО-Транзит"].get(
            7 if transit_term_days <= 7 else
            14 if transit_term_days <= 14 else
            30
        )

class PremiumKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Премиум",
            description="Расширенное покрытие с дополнительными услугами."
        )

    def get_rate(self, vehicle_year, vehicle_price, insurance_variant):
        optima = OptimaProgram()
        base_rate = optima.get_rate(vehicle_year, vehicle_price, insurance_variant)
        return base_rate * values.PREMIUM_COEFF_BASE

    def get_min_premium(self, insurance_variant, has_wheel_disks=False):
        return values.MIN_PREMIUMS_PASSENGER["КАСКО-Премиум"]["WITH_DISKS" if has_wheel_disks else "NO_DISKS"]

AVAILABLE_PROGRAMS = {
    "КАСКО-Оптима": OptimaProgram(),
    "КАСКО-Профит": ProfitProgram(),
    "КАСКО-Автопрофи": AutoprofiProgram(),
    "КАСКО-За полцены": HalfPriceProgram(),
    "КАСКО-за треть цены": ThirdPriceProgram(),
    "КАСКО-Премиум": PremiumKaskoProgram(),
    "Доброе КАСКО": GoodKaskoProgram(),
    "КАСКО-Транзит": TransitKaskoProgram(),
}