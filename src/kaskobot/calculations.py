import math
from datetime import datetime, date 

from src.res import values
from src.res import strings 

def define_age(manufacture_date_str=None, manufacture_year=None):
    """
    Определяет возраст автомобиля в полных годах на основе даты или года выпуска.

    Аргументы:
        manufacture_date_str (str, optional): Дата выпуска автомобиля в формате 'ГГГГ-ММ-ДД'.
                                              Например, '2020-03-15'.
        manufacture_year (int, optional): Год выпуска автомобиля.

    Возвращает:
        int: Возраст автомобиля в полных годах. Возвращает 0, если возраст меньше 1 года.
             Возвращает None, если не предоставлена ни дата, ни год, или если формат неверный.
    """
    today = date.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    if manufacture_date_str:
        try:
            manufacture_date = datetime.strptime(manufacture_date_str, '%Y-%m-%d').date()
            age_years = current_year - manufacture_date.year

            if (current_month < manufacture_date.month) or \
               (current_month == manufacture_date.month and current_day < manufacture_date.day):
                age_years -= 1
            
            return max(0, age_years)

        except ValueError:
            print(f"Предупреждение: Неверный формат даты выпуска: {manufacture_date_str}. Ожидается 'ГГГГ-ММ-ДД'.")
            return None
    elif manufacture_year is not None:
        if not isinstance(manufacture_year, int):
            print(f"Предупреждение: Год выпуска должен быть целым числом, получено {type(manufacture_year)}.")
            return None
        
        age_years = current_year - manufacture_year
        return max(0, age_years) 
    else:
        return None


def get_age_category(age_years, vehicle_type_group):
    if vehicle_type_group in [
        values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
        values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL,
        values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER
    ]:
        if age_years == 0:
            return "до года"
        elif age_years == 1:
            return "1 год"
        elif age_years == 2:
            return "2 года"
        elif age_years == 3:
            return "3 года"
        elif age_years == 4:
            return "4 года"
        elif age_years == 5:
            return "5 лет"
        elif age_years == 6:
            return "6 лет"
        elif age_years == 7:
            return "7 лет"
        # документ не описывает тарифы для возраста более 7 лет для легковых и более 6 лет для грузовых
        if vehicle_type_group == values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK and age_years > 7:
            return "7 лет"
        if vehicle_type_group in [values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL, values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER] and age_years > 6:
            return "6 лет"
    return None


def get_price_category(price, program_name):
    if program_name == "Доброе КАСКО":
        if price <= values.VEHICLE_PRICE_LIMIT_2: # 30000
            return values.VEHICLE_PRICE_LIMIT_2
        elif price <= values.VEHICLE_PRICE_LIMIT_5: # 120000
            return values.VEHICLE_PRICE_LIMIT_5
        else:
            return values.VEHICLE_PRICE_LIMIT_6 # > 120000
    else: # для легковых тс
        if price <= values.VEHICLE_PRICE_LIMIT_1: # 15000
            return values.VEHICLE_PRICE_LIMIT_1
        elif price <= values.VEHICLE_PRICE_LIMIT_2: # 30000
            return values.VEHICLE_PRICE_LIMIT_2
        elif price <= values.VEHICLE_PRICE_LIMIT_3: # 50000
            return values.VEHICLE_PRICE_LIMIT_3
        else:
            return values.VEHICLE_PRICE_LIMIT_4 # > 50000


def calculate_base_tariff(program_name, variant, vehicle_age_years, vehicle_price_usd, vehicle_type_group, truck_subtype=None):
    age_category = get_age_category(vehicle_age_years, vehicle_type_group)
    if not age_category and program_name not in ["Доброе КАСКО"]:
        return None

    tariff_table = None
    if variant == "А":
        if program_name == "КАСКО-Оптима":
            tariff_table = values.OPTIMA_A_RATES
        elif program_name == "КАСКО-Профит":
            tariff_table = values.PROFIT_A_RATES
        elif program_name == "КАСКО-Автопрофи":
            tariff_table = values.AUTOPROFI_A_RATES
        elif program_name == "КАСКО-За полцены":
            tariff_table = values.HALF_PRICE_A_RATES
        elif program_name == "КАСКО-за треть цены":
            tariff_table = values.THIRD_PRICE_A_RATES
        elif program_name == "КАСКО-Премиум":
            base_tariff_optima = values.OPTIMA_A_RATES.get(age_category, {}).get(get_price_category(vehicle_price_usd, program_name))
            return base_tariff_optima * values.PREMIUM_COEFF_BASE if base_tariff_optima else None
        elif program_name == "КАСКО-Транзит":
            tariff_table = values.TRANSIT_A_RATES
        elif program_name == "КАСКО-Бизнес Оптима":
            if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
                tariff_table = values.BUSINESS_OPTIMA_A_RATES
            elif vehicle_type_group == values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER:
                tariff_table = values.BUSINESS_OPTIMA_OVER_8T_A_RATES
        elif program_name == "КАСКО-Бизнес Эконом":
            if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
                tariff_table = values.BUSINESS_ECONOM_A_RATES
            elif vehicle_type_group == values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER:
                tariff_table = values.BUSINESS_ECONOM_OVER_8T_A_RATES

    elif variant == "Б":
        if program_name == "КАСКО-Оптима":
            tariff_table = values.OPTIMA_B_RATES
        elif program_name == "КАСКО-Профит":
            tariff_table = values.PROFIT_B_RATES
        elif program_name == "КАСКО-Автопроfi":
            tariff_table = values.AUTOPROFI_B_RATES
        elif program_name == "КАСКО-За полцены":
            tariff_table = values.HALF_PRICE_B_RATES
        elif program_name == "КАСКО-за треть цены":
            tariff_table = values.THIRD_PRICE_B_RATES
        elif program_name == "КАСКО-Премиум":
            base_tariff_optima = values.OPTIMA_B_RATES.get("all", {}).get(get_price_category(vehicle_price_usd, program_name))
            return base_tariff_optima * values.PREMIUM_COEFF_BASE if base_tariff_optima else None
        elif program_name == "Доброе КАСКО":
            return values.GOOD_KASKO_RATES.get(get_price_category(vehicle_price_usd, program_name))
        elif program_name == "КАСКО-Транзит":
            tariff_table = values.TRANSIT_B_RATES
        elif program_name == "КАСКО-Бизнес Оптима":
            if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
                tariff_table = values.BUSINESS_OPTIMA_B_RATES
            elif vehicle_type_group == values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER:
                tariff_table = values.BUSINESS_OPTIMA_OVER_8T_B_RATES
        elif program_name == "КАСКО-Бизнес Эконом":
            if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
                tariff_table = values.BUSINESS_ECONOM_B_RATES
            elif vehicle_type_group == values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER:
                tariff_table = values.BUSINESS_ECONOM_OVER_8T_B_RATES
    
    if tariff_table is None:
        return None

    if program_name in ["Доброе КАСКО"]:
        return tariff_table
    elif vehicle_type_group in [values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK]:
        price_category = get_price_category(vehicle_price_usd, program_name)
        return tariff_table.get(age_category, {}).get(price_category)
    elif vehicle_type_group in [values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL, values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER]:
        return tariff_table.get(age_category, {}).get(truck_subtype)
    
    return None

def calculate_k_driver(drivers_known, num_drivers, driver_age, driver_exp, is_geely, is_legal_entity_ip, multidrive_2_plus_years_exp):
    k_driver = 1.0

    if drivers_known:
        # Стаж/возраст
        age_group = ""
        if driver_age >= 35:
            age_group = "35_plus"
        elif driver_age >= 25:
            age_group = "25-34"
        else:
            age_group = "16-24"

        exp_group = ""
        if driver_exp >= 2:
            exp_group = "2_plus_years"
        elif driver_exp >= 1:
            exp_group = "1_year"
        else:
            exp_group = "less_1_year"
        
        # для джили данный коэффициент не применяется (п. 3.7.1.1)
        if not is_geely:
            k_driver = values.DRIVER_AGE_EXP_RATES.get(exp_group, {}).get(age_group, 1.0)
    else:
        # Мультидрайв
        if is_legal_entity_ip:
            k_driver = values.MULTIDRIVE_LEGAL_ENTITY_IP
        elif is_geely:
            k_driver = values.MULTIDRIVE_GEELY
        elif multidrive_2_plus_years_exp:
            k_driver = values.MULTIDRIVE_2_PLUS_YEARS_EXP
        else:
            k_driver = values.MULTIDRIVE_STANDARD
    
    return k_driver

def calculate_k_territory(territory_option, vehicle_type_group):
    k_territory = values.TERRITORY_RATE_ALL_TERRITORIES # по умолчанию 1.0

    if territory_option == "Республика Беларусь":
        k_territory = values.TERRITORY_RATE_RB_ONLY # 0.95

    return k_territory


def calculate_k_park(num_vehicles):
    k_park = 1.0
    if num_vehicles >= 15:
        k_park = values.PARK_COEFFS[15]
    elif num_vehicles >= 5:
        k_park = values.PARK_COEFFS[5]
    elif num_vehicles >= 2:
        k_park = values.PARK_COEFFS[2]
    else:
        k_park = values.PARK_COEFFS[1]
    return k_park

def calculate_k_bonus(prev_bonus_class, claims_count):
    k_bonus = values.BONUS_SYSTEM_COEFFS.get(prev_bonus_class, 1.0) # по умолчанию С0 = 1.0

    return k_bonus

def calculate_k_additional(has_other_insurance, other_insurance_amount, vehicle_price_usd, is_credit_leasing_pledge, is_geely, calculation_only_selected):
    k_additional = 1.0
    applied_additional_coeff = False 

    # коэффициент кросселинга (3.7.7.1)
    if has_other_insurance:
        threshold_met = False
        for limit, threshold_amount in sorted(values.CROSSLING_THRESHOLDS.items()):
            if vehicle_price_usd <= limit:
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
            elif limit == values.VEHICLE_PRICE_LIMIT_4 and vehicle_price_usd > limit: # свыше 50000
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
        
        if threshold_met:
            k_additional = values.CROSSLING_COEFF
            applied_additional_coeff = True

    # коэффициент специальной скидки (3.7.7.2) применяется если кросселинг не применился
    if not applied_additional_coeff and has_other_insurance: 
        threshold_met = False
        for limit, threshold_amount in sorted(values.SPECIAL_DISCOUNT_THRESHOLDS.items()):
            if vehicle_price_usd <= limit:
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
            elif limit == values.VEHICLE_PRICE_LIMIT_4 and vehicle_price_usd > limit: # свыше 50000
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
        
        if threshold_met:
            k_additional = values.SPECIAL_DISCOUNT_COEFF
            applied_additional_coeff = True

    if not applied_additional_coeff and is_credit_leasing_pledge and not is_geely:
        k_additional = values.COEFF_CREDIT_LEASING_PLEDGE
        applied_additional_coeff = True 

    return k_additional

def calculate_final_premium(data):
    program_name = data.get("program")
    variant = data.get("variant")
    vehicle_age_years = data.get("vehicle_age_years")
    vehicle_price_usd = data.get("vehicle_price_usd")
    vehicle_type_group = data.get("vehicle_type_group")
    truck_subtype = data.get("truck_subtype") # для грузовых ТС

    # базовый тариф
    base_tariff = calculate_base_tariff(program_name, variant, vehicle_age_years, vehicle_price_usd, vehicle_type_group, truck_subtype)
    if base_tariff is None:
        return None 

    total_tariff = base_tariff / 100 

    k_driver = 1.0
    # применяется только для легковых ТС
    if vehicle_type_group == values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
        k_driver = calculate_k_driver(
            data.get("drivers_known"),
            data.get("num_drivers"),
            data.get("driver_age"),
            data.get("driver_exp"),
            data.get("is_geely"),
            data.get("is_legal_entity_ip"),
            data.get("multidrive_2_plus_years_exp")
        )
    total_tariff *= k_driver

    # коэффициент за территорию (3.7.2)
    k_territory = calculate_k_territory(data.get("territory"), vehicle_type_group)
    if vehicle_type_group in [values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL, values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER] and \
       data.get("territory") == "Республика Беларусь и за ее пределами":
        total_tariff /= 0.95
    else:
        total_tariff *= k_territory 

    # коэффициент превышения норматива обращений (3.7.3)
    if data.get("exceeding_claims_norm"):
        total_tariff *= values.COEFF_EXCEEDING_CLAIMS_NORM

    # коэффициент за парк (3.7.4)
    if data.get("num_vehicles_insured") is not None:
        total_tariff *= calculate_k_park(data.get("num_vehicles_insured"))

    # коэффициент системы "Бонус" (3.7.5)
    # не применяется для "Доброе КАСКО" и "КАСКО-Транзит"
    if program_name not in ["Доброе КАСКО", "КАСКО-Транзит"]:
        total_tariff *= calculate_k_bonus(data.get("bonus_class"), data.get("claims_count"))

    # коэффициент "выплата только на основании калькуляции" (3.7.6)
    # только для варианта А
    # не допускается одновременное применение с "Лицензионные детали"
    if data.get("calculation_only") and variant == "А" and not data.get("licensed_parts"):
        total_tariff *= values.COEFF_CALCULATION_ONLY

    # доп коэффициенты (3.7.7) 
    total_tariff *= calculate_k_additional(
        data.get("has_other_insurance"),
        data.get("other_insurance_amount"),
        vehicle_price_usd,
        data.get("credit_leasing_pledge"),
        data.get("is_geely"),
        data.get("calculation_only")
    )

    # коэффициенты доп опций (3.7.8) - только для варианта А
    if data.get("additional_options") and variant == "А":
        total_tariff *= values.COEFF_ADDITIONAL_OPTIONS
    if data.get("is_taxi_uber"):
        total_tariff *= values.COEFF_TAXI_UBER
    if data.get("is_employee"):
        total_tariff *= values.COEFF_EMPLOYEE
    if data.get("satellite_alarm"):
        total_tariff *= values.COEFF_SATELLITE_ALARM
    if data.get("marking"):
        total_tariff *= values.COEFF_MARKING
    if data.get("is_geely"):
        total_tariff *= values.COEFF_GEELY
    if data.get("single_payment"):
        total_tariff *= values.COEFF_SINGLE_PAYMENT
    if data.get("licensed_parts") and variant == "А" and vehicle_age_years >= 3 and not data.get("calculation_only"):
        total_tariff *= values.COEFF_LICENSED_PARTS

    # коэффициент при включении в договор страхования риска повреждения колесных дисков (3.7.12)
    # только для  "КАСКО-Премиум"
    if program_name == "КАСКО-Премиум" and data.get("wheel_disks"):
        if vehicle_price_usd <= values.VEHICLE_PRICE_LIMIT_7: # до 70 000 $ вкл.
            total_tariff *= values.COEFF_WHEEL_DISKS_LT_70K
        else: # свыше 70 000 $
            total_tariff *= values.COEFF_WHEEL_DISKS_GT_70K
    
    # коэффициент краткосрочности (3.9.2.8) только для "КАСКО-Транзит"
    if program_name == "КАСКО-Транзит":
        term_days = data.get("transit_term_days")
        if term_days <= 7:
            total_tariff *= values.SHORT_TERM_COEFFS[7]
        elif term_days <= 14:
            total_tariff *= values.SHORT_TERM_COEFFS[14]
        else: # 15-30 дней
            total_tariff *= values.SHORT_TERM_COEFFS[30]

    total_tariff = round(total_tariff, 4) 

    # расчет страхового взноса
    if program_name == "КАСКО-Премиум":
        # СВ = СС * (СТ * К1…* Кn *1,05) + ДУ
        # 1.05 уже учтен в calculate_base_tariff для Премиум.
        # поэтому формула будет: СВ = СС * (СТ_базовый_оптима * все_коэффициенты) + ДУ
        # total_tariff уже содержит base_tariff_optima * 1.05 * все_коэффициенты
        premium_amount = (vehicle_price_usd * total_tariff) + values.PREMIUM_ADD_SERVICES_COST
    else:
        premium_amount = vehicle_price_usd * total_tariff

    # применение минимального страхового взноса (3.6, 4.4, 5.4)
    min_premium = get_min_premium(data)

    final_premium = max(premium_amount, min_premium)

    if data.get("is_employee") and premium_amount < min_premium:
        final_premium = min_premium * values.COEFF_EMPLOYEE 
        if program_name not in ["Доброе КАСКО", "КАСКО-Транзит"]: 
             final_premium *= calculate_k_bonus(data.get("bonus_class"), data.get("claims_count"))

    final_premium = round(final_premium)

    return final_premium


def get_min_premium(data):
    program_name = data.get("program")
    variant = data.get("variant")
    vehicle_age_years = data.get("vehicle_age_years")
    vehicle_type_group = data.get("vehicle_type_group")
    truck_subtype = data.get("truck_subtype")
    has_wheel_disks = data.get("wheel_disks")
    transit_term_days = data.get("transit_term_days")
    if program_name in ["КАСКО-Оптима", "КАСКО-Профит"]:
        if vehicle_age_years <= 3 and data.get("drivers_known") and data.get("driver_age") >= 35 and data.get("driver_exp") >= 2 and variant == "А":
            if (data.get("is_geely") and data.get("multidrive_2_plus_years_exp")) or (not data.get("is_geely")):
                return values.MIN_PREMIUMS_PASSENGER[program_name]["А_SHORT_TERM"]
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-Автопрофи":
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-За полцены":
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-за треть цены":
        return values.MIN_PREMIUMS_PASSENGER[program_name]
    elif program_name == "КАСКО-Премиум":
        if has_wheel_disks:
            return values.MIN_PREMIUMS_PASSENGER[program_name]["WITH_DISKS"]
        else:
            return values.MIN_PREMIUMS_PASSENGER[program_name]["NO_DISKS"]
    elif program_name == "Доброе КАСКО":
        return values.MIN_PREMIUMS_PASSENGER[program_name]
    elif program_name == "КАСКО-Транзит":
        if transit_term_days <= 7:
            return values.MIN_PREMIUMS_PASSENGER[program_name][7]
        elif transit_term_days <= 14:
            return values.MIN_PREMIUMS_PASSENGER[program_name][14]
        else: # 15-30 дней
            return values.MIN_PREMIUMS_PASSENGER[program_name][30]
    elif program_name == "КАСКО-Бизнес Оптима":
        if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
            return values.MIN_PREMIUMS_BUSINESS_1_5_8T[program_name][variant].get(truck_subtype)
        elif vehicle_type_group == values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER:
            if variant == "А":
                return values.MIN_PREMIUMS_BUSINESS_OVER_8T[program_name][variant].get(truck_subtype)
            elif variant == "Б":
                return values.MIN_PREMIUMS_BUSINESS_OVER_8T[program_name][variant]["ALL_CATEGORIES"] # для Б всех категорий один минимальный
    elif program_name == "КАСКО-Бизнес Эконом":
        if vehicle_type_group == values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL:
            return values.MIN_PREMIUMS_BUSINESS_1_5_8T[program_name][variant].get(truck_subtype)

    return 0 

# вспомогательная функция для определения класса по сумме (для кросселинга/спецскидки)
def get_cross_discount_price_category(price):
    if price <= values.VEHICLE_PRICE_LIMIT_1: # 15000
        return values.VEHICLE_PRICE_LIMIT_1
    elif price <= values.VEHICLE_PRICE_LIMIT_2: # 30000
        return values.VEHICLE_PRICE_LIMIT_2
    elif price <= values.VEHICLE_PRICE_LIMIT_3: # 50000
        return values.VEHICLE_PRICE_LIMIT_3
    else: # > 50000
        return values.VEHICLE_PRICE_LIMIT_4