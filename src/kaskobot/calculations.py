import math
from datetime import date, datetime
from src.res import values
from src.res import strings

def is_promo_campaign_active():
    """Проверяет, активна ли рекламная кампания"""
    current_date = date.today()
    start_date = datetime.strptime(values.PROMO_CAMPAIGN_START, "%Y-%m-%d").date()
    end_date = datetime.strptime(values.PROMO_CAMPAIGN_END, "%Y-%m-%d").date()
    return start_date <= current_date <= end_date

def define_age(manufacture_year=None):
    if manufacture_year is None or not isinstance(manufacture_year, int):
        return None, False, f"Ошибка: Год выпуска должен быть целым числом, получено {manufacture_year}."

    current_date = date.today()
    current_year = current_date.year
    current_month = current_date.month
    
    # Всегда максимальный возраст 7 лет
    max_vehicle_age = 7
    min_allowed_year = current_year - max_vehicle_age

    if manufacture_year < min_allowed_year:
        return None, False, "AGE_EXCEEDED"
    
    if manufacture_year > current_year:
        return None, False, f"Ошибка: Год выпуска не может быть больше {current_year}."

    is_new_vehicle = (manufacture_year == current_year)
    
    age = current_year - manufacture_year
    if not is_new_vehicle and current_month < 7:
        age -= 1
    if is_new_vehicle:
        age = 0
    
    return max(0, min(age, max_vehicle_age)), is_new_vehicle, ""

def check_vehicle_age_eligibility(program_name, vehicle_age_years):
    max_age = 7
    if vehicle_age_years > max_age:
        return False, f"Возраст ТС превышает {max_age} лет, страхование недоступно."
    return True, ""

def get_age_category(age_years, vehicle_type_group):
    if vehicle_type_group != values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
        return None, "Тип ТС не поддерживается."
    if age_years == 0:
        return "до года", ""
    elif age_years == 1:
        return "1 год", ""
    elif age_years == 2:
        return "2 года", ""
    elif age_years == 3:
        return "3 года", ""
    elif age_years == 4:
        return "4 года", ""
    elif age_years == 5:
        return "5 лет", ""
    elif age_years == 6:
        return "6 лет", ""
    elif age_years >= 7:
        return "7 лет", ""
    return None, "Недопустимый возраст ТС."

def get_price_category(price, program_name):
    if price <= values.VEHICLE_PRICE_LIMIT_1:
        return values.VEHICLE_PRICE_LIMIT_1
    elif price <= values.VEHICLE_PRICE_LIMIT_2:
        return values.VEHICLE_PRICE_LIMIT_2
    elif price <= values.VEHICLE_PRICE_LIMIT_3:
        return values.VEHICLE_PRICE_LIMIT_3
    return values.VEHICLE_PRICE_LIMIT_4

def calculate_base_tariff(program_name, vehicle_age_years, vehicle_price_usd, vehicle_type_group):
    if vehicle_type_group != values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
        return None, "Расчет доступен только для легковых автомобилей."

    is_eligible, error_message = check_vehicle_age_eligibility(program_name, vehicle_age_years)
    if not is_eligible:
        return None, error_message

    age_category, error_message = get_age_category(vehicle_age_years, vehicle_type_group)
    if not age_category:
        return None, error_message

    tariff_table = {
        "КАСКО-Оптима": values.OPTIMA_A_RATES,
        "КАСКО-Профит": values.PROFIT_A_RATES,
        "КАСКО-Премиум": values.OPTIMA_A_RATES
    }.get(program_name)

    if tariff_table is None:
        return None, f"Тарифная таблица не определена для программы {program_name}."

    price_category = get_price_category(vehicle_price_usd, program_name)
    tariff = tariff_table.get(age_category, {}).get(price_category)
    if tariff is None:
        return None, f"Тариф не найден для категории возраста {age_category} и стоимости {price_category} в программе {program_name}."
    return tariff, ""

def calculate_k_driver(drivers_known, drivers_data, is_geely, is_multidrive):
    if is_geely:
        # Для GEELY: только по стажу (возраст не учитывается)
        if not drivers_data or len(drivers_data) == 0:
            return values.MULTIDRIVE_GEELY_LESS_2_YEARS
        
        driver_exp = drivers_data[0]["experience"]
        
        if driver_exp >= 2:
            return values.MULTIDRIVE_GEELY_2_PLUS_YEARS
        else:
            return values.MULTIDRIVE_GEELY_LESS_2_YEARS
    
    if not drivers_data or len(drivers_data) == 0:
        return values.MULTIDRIVE_STANDARD
    
    driver_age = drivers_data[0]["age"]
    driver_exp = drivers_data[0]["experience"]
    
    age_group = "16-24" if driver_age <= 24 else "25-34" if driver_age <= 34 else "35_plus"
    exp_group = "less_1_year" if driver_exp < 1 else "1_year" if driver_exp == 1 else "2_plus_years"
    
    base_coeff = values.DRIVER_AGE_EXP_RATES.get(exp_group, {}).get(age_group, 1.0)
    
    if is_multidrive:
        if driver_exp >= 2:
            return values.MULTIDRIVE_2_PLUS_YEARS_EXP
        else:
            return values.MULTIDRIVE_STANDARD
    
    return base_coeff

def calculate_k_territory(territory_option, vehicle_type_group):
    if territory_option == "Республика Беларусь":
        return values.TERRITORY_RATE_RB_ONLY
    return values.TERRITORY_RATE_ALL_TERRITORIES

def check_promo_eligibility(is_in_list):
    """Проверяет соответствие условиям рекламной акции"""
    if not is_promo_campaign_active():
        return False
    
    if not is_in_list:
        return False
    
    return True

def calculate_final_premium(data):
    try:
        program_name = data.get("program")
        vehicle_age_years = data.get("vehicle_age_years")
        vehicle_price_usd = data.get("vehicle_price_usd")
        vehicle_type_group = data.get("vehicle_type_group")
        drivers_known = data.get("drivers_known", False)
        drivers_data = data.get("drivers_data", [])
        is_geely = data.get("is_geely", False)
        is_multidrive = data.get("is_multidrive", False)
        territory = data.get("territory")
        credit_leasing_pledge = data.get("credit_leasing_pledge", False)
        licensed_parts = data.get("licensed_parts", False)
        quarterly_payment = data.get("quarterly_payment", False)
        is_in_list = data.get("is_in_list", False)

        if not all([program_name, vehicle_age_years is not None, vehicle_price_usd, vehicle_type_group, territory]):
            return None, f"Недостаточно данных для расчета: {data}"

        if vehicle_type_group != values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
            return None, "Расчет доступен только для легковых автомобилей."

        base_tariff, error_message = calculate_base_tariff(program_name, vehicle_age_years, vehicle_price_usd, vehicle_type_group)
        if base_tariff is None:
            return None, error_message

        total_tariff = base_tariff / 100
        
        total_tariff *= calculate_k_driver(drivers_known, drivers_data, is_geely, is_multidrive)
        
        total_tariff *= calculate_k_territory(territory, vehicle_type_group)

        if credit_leasing_pledge:
            total_tariff *= values.CREDIT_LEASING_PLEDGE_COEFF

        # Применение коэффициентов согласно приказу O0090
        promo_eligible = check_promo_eligibility(is_in_list)
        
        if is_geely:
            # Для GEELY: 0.75 * 0.9 = 0.675
            total_tariff *= values.COEFF_GEELY
            if promo_eligible:
                total_tariff *= values.COEFF_PROMO_CAMPAIGN
        elif promo_eligible and is_in_list:
            # Для автомобилей из списка акции: 0.9
            total_tariff *= values.COEFF_PROMO_CAMPAIGN
        # Для остальных (не в списке, не GEELY): коэффициент 1.0 (не применяется)
            
        if licensed_parts and program_name in ["КАСКО-Оптима", "КАСКО-Профит"] and vehicle_age_years >= 3:
            total_tariff *= values.COEFF_LICENSED_PARTS

        if program_name == "КАСКО-Премиум":
            total_tariff *= values.PREMIUM_COEFF_BASE

        premium_amount = vehicle_price_usd * total_tariff
        
        if program_name == "КАСКО-Премиум":
            premium_amount += values.PREMIUM_ADD_SERVICES_COST

        # Сначала применяем коэффициент разовой оплаты к базовой сумме
        premium_with_onetime_discount = premium_amount * values.COEFF_ONE_TIME_PAYMENT
        
        # Для ежеквартальной - берем разовую сумму (которая уже 100%) и добавляем 10%
        if quarterly_payment:
            # Ежеквартальная = разовая × 1.1 (разовая воспринимается как 100%)
            final_premium = premium_with_onetime_discount * values.COEFF_QUARTERLY_PAYMENT
        else:
            final_premium = premium_with_onetime_discount

        min_premium = values.MIN_PREMIUMS_PASSENGER.get(program_name)
        final_premium = max(final_premium, min_premium) if min_premium is not None else final_premium

        return round(final_premium), ""
    except Exception as e:
        return None, f"Ошибка при расчете премии: {str(e)}"

def calculate_quarterly_premium(final_premium):
    """Не используется - расчет происходит в calculate_final_premium с quarterly_payment=True"""
    quarterly_premium = final_premium * values.COEFF_QUARTERLY_PAYMENT
    return round(quarterly_premium)