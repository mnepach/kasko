from ..res import values as values
from . import calculations as calc

class BaseProgram:
    _name = ""
    _description = "" 
    _type_of_rates = "standard" 
    _min_premium_a = 0.0
    _min_premium_b = 0.0
    _price_limits = [ 
        values.VEHICLE_PRICE_LIMIT_1,
        values.VEHICLE_PRICE_LIMIT_2,
        values.VEHICLE_PRICE_LIMIT_3,
        values.VEHICLE_PRICE_LIMIT_4 
    ] 
    _is_truck_program = False 

    def __init__(self, rates_a=None, rates_b=None, name="", description="", is_truck_program=False):
        self._rates_a = rates_a
        self._rates_b = rates_b
        self._name = name
        self._description = description
        self._is_truck_program = is_truck_program

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def is_truck_program(self):
        return self._is_truck_program

    def get_rate(self, vehicle_year, vehicle_price, insurance_variant, transit_term_days=None, truck_type=None):
        """
        Метод для получения базового тарифа программы.
        Переопределяется для специальных программ (GoodKasko, Transit, Business).
        """
        rates_to_use = self._rates_a if insurance_variant == "A" else self._rates_b
        if not rates_to_use:
            raise ValueError(f"Для программы {self._name} и варианта {insurance_variant} тарифы не заданы.")

        _age_key = self._define_vehicle_age_key(vehicle_year)
        
        # специальная логика для грузовых программ, где тарифы зависят от truck_type
        if self._is_truck_program:
            if truck_type is None:
                raise ValueError(f"Для грузовой программы '{self._name}' необходимо указать тип грузового ТС (truck_type).")
            if _age_key not in rates_to_use or truck_type not in rates_to_use[_age_key]:
                 raise ValueError(f"Невозможно найти тариф для грузовой программы {self._name} с данными: "
                                  f"возраст ТС '{_age_key}', тип ТС '{truck_type}'.")
            return rates_to_use[_age_key][truck_type]
        else:
            _price_key = self._define_price_key(vehicle_price, self._price_limits)
            if _age_key not in rates_to_use or _price_key not in rates_to_use[_age_key]:
                 raise ValueError(f"Невозможно найти тариф для легковой программы {self._name} с данными: "
                                  f"возраст ТС '{_age_key}', цена '{vehicle_price}'.")
            return rates_to_use[_age_key][_price_key]

    def get_min_premium(self, insurance_variant, transit_term_days=None, truck_type=None):
        """Возвращает минимальный страховой взнос для программы и варианта."""
        
        if self._name == "КАСКО-Транзит":
            if transit_term_days is None: 
                return 0.0 
            elif transit_term_days <= 7: 
                return values.MIN_PREMIUMS_PASSENGER["КАСКО-Транзит"][7]
            elif transit_term_days <= 14: 
                return values.MIN_PREMIUMS_PASSENGER["КАСКО-Транзит"][14]
            else: # 15-30 дней
                return values.MIN_PREMIUMS_PASSENGER["КАСКО-Транзит"][30] 
        elif self._name == "КАСКО-Премиум":
            return 0.0 
        elif self._name == "Доброе КАСКО":
            return values.MIN_PREMIUMS_PASSENGER["Доброе КАСКО"]
        
        # логика для бизнес-программ с учетом truck_type (требует доработки)
        elif self._name == "КАСКО-Бизнес Оптима":
            if truck_type:
                if truck_type in values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Оптима"]["А"]:
                    return values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Оптима"][insurance_variant][truck_type]
                elif truck_type in values.MIN_PREMIUMS_BUSINESS_OVER_8T["КАСКО-Бизнес Оптима"]["А"]:
                    if insurance_variant == "Б":
                        return values.MIN_PREMIUMS_BUSINESS_OVER_8T["КАСКО-Бизнес Оптима"]["Б"]["ALL_CATEGORIES"]
                    return values.MIN_PREMIUMS_BUSINESS_OVER_8T["КАСКО-Бизнес Оптима"][insurance_variant][truck_type]
                else:
                    return 0.0 
            return values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Оптима"][insurance_variant].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0) # Пример
        
        elif self._name == "КАСКО-Бизнес Эконом":
            if truck_type:
                if truck_type in values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Эконом"]["А"]:
                    return values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Эконом"][insurance_variant][truck_type]
                else:
                     return 0.0 
            return values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Эконом"][insurance_variant].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0) # Пример
        
        return self._min_premium_a if insurance_variant == "A" else self._min_premium_b

    def _define_vehicle_age_key(self, vehicle_year):
        """Определяет строковый ключ возраста ТС для словарей тарифов."""
        _age_in_years = calc.define_age(vehicle_year)
        
        if self._is_truck_program: 
            if _age_in_years == 0: return "до года"
            elif _age_in_years == 1: return "1 год"
            elif _age_in_years == 2: return "2 года"
            elif _age_in_years == 3: return "3 года"
            elif _age_in_years == 4: return "4 года"
            elif _age_in_years == 5: return "5 лет"
            elif _age_in_years == 6: return "6 лет"
            else: return "6 лет" 
        else: 
            if _age_in_years == 0: return "до года"
            elif _age_in_years == 1: return "1 год"
            elif _age_in_years == 2: return "2 года"
            elif _age_in_years == 3: return "3 года"
            elif _age_in_years == 4: return "4 года"
            elif _age_in_years == 5: return "5 лет"
            elif _age_in_years == 6: return "6 лет"
            elif _age_in_years == 7: return "7 лет"
            else: return "7 лет" 

    def _define_price_key(self, vehicle_price, price_limits):
        """Определяет ключевое значение для тарифа на основе стоимости ТС и заданных лимитов."""
        if vehicle_price <= price_limits[0]:
            return price_limits[0]
        elif len(price_limits) > 1 and vehicle_price <= price_limits[1]:
            return price_limits[1]
        elif len(price_limits) > 2 and vehicle_price <= price_limits[2]:
            return price_limits[2]
        elif len(price_limits) > 3 and vehicle_price <= price_limits[3]:
            return price_limits[3]
        elif len(price_limits) > 4 and vehicle_price <= price_limits[4]: 
            return price_limits[4]
        elif len(price_limits) > 5 and vehicle_price <= price_limits[5]: 
            return price_limits[5]
        else: 
            return price_limits[-1]


# --- Конкретные классы программ ---

class OptimaProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.OPTIMA_A_RATES,
            rates_b=values.OPTIMA_B_RATES,
            name="КАСКО-Оптима",
            description="Полное КАСКО без франшизы по рискам повреждения ТС. "
                        "Оплата возмещения без учета износа (Вариант А) или с учетом износа (Вариант Б). "
                        "Минимальный взнос: 600$ (А), 400$ (Б)."
        )
        self._min_premium_a = values.MIN_PREMIUMS_PASSENGER["КАСКО-Оптима"]["А"]
        self._min_premium_b = values.MIN_PREMIUMS_PASSENGER["КАСКО-Оптима"]["Б"]

class ProfitProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.PROFIT_A_RATES,
            rates_b=values.PROFIT_B_RATES,
            name="КАСКО-Профит",
            description="Полное КАСКО без франшизы по рискам повреждения ТС. "
                        "Отдельные условия по обращениям без документов. "
                        "Минимальный взнос: 600$ (А), 400$ (Б)."
        )
        self._min_premium_a = values.MIN_PREMIUMS_PASSENGER["КАСКО-Профит"]["А"]
        self._min_premium_b = values.MIN_PREMIUMS_PASSENGER["КАСКО-Профит"]["Б"]

class AutoprofiProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.AUTOPROFI_A_RATES,
            rates_b=values.AUTOPROFI_B_RATES,
            name="КАСКО-Автопрофи",
            description="Полное КАСКО с безусловной франшизой 200$ по рискам повреждения ТС. "
                        "Минимальный взнос: 400$ (А), 300$ (Б)."
        )
        self._min_premium_a = values.MIN_PREMIUMS_PASSENGER["КАСКО-Автопрофи"]["А"]
        self._min_premium_b = values.MIN_PREMIUMS_PASSENGER["КАСКО-Автопрофи"]["Б"]

class HalfPriceProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.HALF_PRICE_A_RATES,
            rates_b=values.HALF_PRICE_B_RATES,
            name="КАСКО-За полцены",
            description="Полное КАСКО с франшизой 500$ (до 50k$) или 700$ (свыше 50k$). "
                        "Минимальный взнос: 300$ (А), 200$ (Б)."
        )
        self._min_premium_a = values.MIN_PREMIUMS_PASSENGER["КАСКО-За полцены"]["А"]
        self._min_premium_b = values.MIN_PREMIUMS_PASSENGER["КАСКО-За полцены"]["Б"]

class ThirdPriceProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.THIRD_PRICE_A_RATES,
            rates_b=values.THIRD_PRICE_B_RATES,
            name="КАСКО-за треть цены",
            description="Полное КАСКО с франшизой 1000$ (до 50k$) или 1500$ (свыше 50k$). "
                        "Минимальный взнос: 300$."
        )
        self._min_premium_a = values.MIN_PREMIUMS_PASSENGER["КАСКО-за треть цены"]
        self._min_premium_b = values.MIN_PREMIUMS_PASSENGER["КАСКО-за треть цены"] 

class GoodKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="Доброе КАСКО",
            description="Страхование только от полной гибели и хищения ТС. "
                        "Только Вариант Б. Без франшиз. "
                        "Минимальный взнос: 100$."
        )
        self._type_of_rates = "good_kasko"
        self._price_limits = [
            values.VEHICLE_PRICE_LIMIT_2, # до 30 000 $ вкл.
            values.VEHICLE_PRICE_LIMIT_5, # свыше 30 000 $ до 120 000 $ вкл.
            values.VEHICLE_PRICE_LIMIT_6  # свыше 120 000 $
        ]
    
    def get_rate(self, vehicle_year, vehicle_price, insurance_variant, transit_term_days=None, truck_type=None):
        if insurance_variant == "A": 
            raise ValueError("Доброе КАСКО доступно только для Варианта Б.")

        price_key = None
        if vehicle_price <= values.VEHICLE_PRICE_LIMIT_2:
            price_key = values.VEHICLE_PRICE_LIMIT_2
        elif vehicle_price <= values.VEHICLE_PRICE_LIMIT_5:
            price_key = values.VEHICLE_PRICE_LIMIT_5
        elif vehicle_price >= values.VEHICLE_PRICE_LIMIT_6:
            price_key = values.VEHICLE_PRICE_LIMIT_6 
        else: 
            price_key = values.VEHICLE_PRICE_LIMIT_5 

        if price_key not in values.GOOD_KASKO_RATES:
            raise ValueError(f"Невозможно найти тариф для Доброго КАСКО для цены {vehicle_price}.")
        
        return values.GOOD_KASKO_RATES[price_key]

class TransitKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.TRANSIT_A_RATES,
            rates_b=values.TRANSIT_B_RATES,
            name="КАСКО-Транзит",
            description="Для ТС с транзитными номерами или следующих транзитом. "
                        "Риски повреждения ТС. "
                        "Короткие сроки (от 1 дня до 1 месяца). "
                        "Есть свой коэффициент краткосрочности."
        )
        self._type_of_rates = "transit"
    
    def get_rate(self, vehicle_year, vehicle_price, insurance_variant, transit_term_days=None, truck_type=None):
        base_rate = super().get_rate(vehicle_year, vehicle_price, insurance_variant, transit_term_days, truck_type)
        
        coeff_short_term = 1.0
        if transit_term_days is not None:
            if transit_term_days <= 7:
                coeff_short_term = values.SHORT_TERM_COEFFS[7]
            elif transit_term_days <= 14:
                coeff_short_term = values.SHORT_TERM_COEFFS[14]
            elif transit_term_days <= 30: # До 1 месяца, ключ 30
                coeff_short_term = values.SHORT_TERM_COEFFS[30]
            else:
                 raise ValueError("Срок для КАСКО-Транзит должен быть от 1 до 30 дней.")
        
        return base_rate * coeff_short_term


class PremiumKaskoProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            name="КАСКО-Премиум",
            description="Расширенное покрытие с дополнительными услугами (аренда авто, юр. расходы, буксировка). "
                        "Базовый тариф рассчитывается как для КАСКО-Оптима + 1.05 и доп. услуги. "
                        "Минимальный взнос: 1500$ (без дисков), 1900$ (с дисками)."
        )
        self._type_of_rates = "premium"
        self._min_premium_no_disks = values.MIN_PREMIUMS_PASSENGER["КАСКО-Премиум"]["NO_DISKS"]
        self._min_premium_with_disks = values.MIN_PREMIUMS_PASSENGER["КАСКО-Премиум"]["WITH_DISKS"]
    
    def get_rate(self, vehicle_year, vehicle_price, insurance_variant, transit_term_days=None, truck_type=None):
        optima_base_program = OptimaProgram()
        base_rate = optima_base_program.get_rate(vehicle_year, vehicle_price, insurance_variant, transit_term_days, truck_type)
        return base_rate

    def get_min_premium(self, insurance_variant=None, transit_term_days=None, truck_type=None, has_wheel_disks_risk=False):
        if has_wheel_disks_risk:
            return self._min_premium_with_disks
        return self._min_premium_no_disks


class BusinessOptimaProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.BUSINESS_OPTIMA_A_RATES,
            rates_b=values.BUSINESS_OPTIMA_B_RATES,
            name="КАСКО-Бизнес Оптима",
            description="Программа для грузовых ТС, прицепов, полуприцепов. Полное КАСКО без франшизы. "
                        "Минимальный взнос: 700$ (А), 500$ (Б).",
            is_truck_program=True
        )

        self._min_premium_a = values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Оптима"]["А"].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0)
        self._min_premium_b = values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Оптима"]["Б"].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0)


class BusinessEconomProgram(BaseProgram):
    def __init__(self):
        super().__init__(
            rates_a=values.BUSINESS_ECONOM_A_RATES,
            rates_b=values.BUSINESS_ECONOM_B_RATES,
            name="КАСКО-Бизнес Эконом",
            description="Программа для грузовых ТС, прицепов, полуприцепов. Полное КАСКО с франшизой. "
                        "Минимальный взнос: 700$ (А), 500$ (Б).",
            is_truck_program=True
        )

        self._min_premium_a = values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Эконом"]["А"].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0)
        self._min_premium_b = values.MIN_PREMIUMS_BUSINESS_1_5_8T["КАСКО-Бизнес Эконом"]["Б"].get(values.TRUCK_TYPE_1_5_8T_MICROBUS, 0.0)


# --- Список доступных программ ---

AVAILABLE_PROGRAMS = {
    "КАСКО-Оптима": OptimaProgram(),
    "КАСКО-Профит": ProfitProgram(),
    "КАСКО-Автопрофи": AutoprofiProgram(),
    "КАСКО-За полцены": HalfPriceProgram(),
    "КАСКО-за треть цены": ThirdPriceProgram(),
    "КАСКО-Премиум": PremiumKaskoProgram(),
    "Доброе КАСКО": GoodKaskoProgram(),
    "КАСКО-Транзит": TransitKaskoProgram(),
    "КАСКО-Бизнес Оптима": BusinessOptimaProgram(),
    "КАСКО-Бизнес Эконом": BusinessEconomProgram(),
}