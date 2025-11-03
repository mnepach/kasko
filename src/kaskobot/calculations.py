import math
from datetime import date
from src.res import values
from src.res import strings

def define_age(manufacture_year=None, is_new_vehicle=False):
    if manufacture_year is None or not isinstance(manufacture_year, int):
        return None, f"Ошибка: Год выпуска должен быть целым числом, получено {manufacture_year}."

    current_date = date.today()
    current_year = current_date.year
    current_month = current_date.month
    max_vehicle_age = 7
    min_allowed_year = current_year - max_vehicle_age

    if manufacture_year < min_allowed_year or manufacture_year > current_year:
        return None, f"Ошибка: Год выпуска должен быть от {min_allowed_year} до {current_year}."

    age = current_year - manufacture_year
    if not is_new_vehicle and current_month < 7:
        age -= 1
    if is_new_vehicle and manufacture_year >= current_year:
        age = 0
    return max(0, min(age, max_vehicle_age)), ""

def check_vehicle_age_eligibility(program_name, vehicle_age_years):
    if vehicle_age_years > 7:
        return False, "Возраст ТС превышает 7 лет, страхование недоступно."
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

def calculate_k_driver(drivers_known, num_drivers, drivers_data, is_geely, multidrive_2_plus_years_exp):
    if drivers_known and not is_geely and drivers_data:
        driver_age = drivers_data[0]["age"]
        driver_exp = drivers_data[0]["experience"]
        age_group = "16-24" if driver_age <= 24 else "25-34" if driver_age <= 34 else "35_plus"
        exp_group = "less_1_year" if driver_exp < 1 else "1_year" if driver_exp == 1 else "2_plus_years"
        return values.DRIVER_AGE_EXP_RATES.get(exp_group, {}).get(age_group, 1.0)
    if is_geely:
        return values.MULTIDRIVE_GEELY
    if multidrive_2_plus_years_exp:
        return values.MULTIDRIVE_2_PLUS_YEARS_EXP
    return values.MULTIDRIVE_STANDARD

def calculate_k_territory(territory_option, vehicle_type_group):
    if territory_option == "Республика Беларусь":
        return values.TERRITORY_RATE_RB_ONLY
    return values.TERRITORY_RATE_ALL_TERRITORIES

def calculate_final_premium(data):
    try:
        program_name = data.get("program")
        vehicle_age_years = data.get("vehicle_age_years")
        vehicle_price_usd = data.get("vehicle_price_usd")
        vehicle_type_group = data.get("vehicle_type_group")
        drivers_known = data.get("drivers_known", False)
        num_drivers = data.get("num_drivers", 1)
        drivers_data = data.get("drivers_data", [])
        is_geely = data.get("is_geely", False)
        territory = data.get("territory")
        credit_leasing_pledge = data.get("credit_leasing_pledge", False)
        licensed_parts = data.get("licensed_parts", False)
        quarterly_payment = data.get("quarterly_payment", False)
        geely_low_exp_coeff = data.get("geely_low_exp_coeff", 1.0)
        is_in_list = data.get("is_in_list", False)

        if not all([program_name, vehicle_age_years is not None, vehicle_price_usd, vehicle_type_group, territory]):
            return None, f"Недостаточно данных для расчета: {data}"

        if vehicle_type_group != values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
            return None, "Расчет доступен только для легковых автомобилей."

        base_tariff, error_message = calculate_base_tariff(program_name, vehicle_age_years, vehicle_price_usd, vehicle_type_group)
        if base_tariff is None:
            return None, error_message

        total_tariff = base_tariff / 100
        total_tariff *= calculate_k_driver(drivers_known, num_drivers, drivers_data, is_geely, data.get("multidrive_2_plus_years_exp", False))
        total_tariff *= calculate_k_territory(territory, vehicle_type_group)

        if credit_leasing_pledge and not is_geely:
            total_tariff *= values.CREDIT_LEASING_PLEDGE_COEFF

        if is_geely:
            total_tariff *= values.COEFF_GEELY
        total_tariff *= values.COEFF_IN_LIST if is_in_list else values.COEFF_NOT_IN_LIST

        if licensed_parts and program_name in ["КАСКО-Оптима", "КАСКО-Профит"] and vehicle_age_years >= 3:
            total_tariff *= values.COEFF_LICENSED_PARTS

        if program_name == "КАСКО-Премиум":
            total_tariff *= values.PREMIUM_COEFF_BASE

        premium_amount = vehicle_price_usd * total_tariff
        if program_name == "КАСКО-Премиум":
            premium_amount += values.PREMIUM_ADD_SERVICES_COST

        if quarterly_payment:
            premium_amount *= values.COEFF_QUARTERLY_PAYMENT
        else:
            premium_amount *= values.COEFF_ONE_TIME_PAYMENT

        min_premium = values.MIN_PREMIUMS_PASSENGER.get(program_name)
        final_premium = max(premium_amount, min_premium) if min_premium is not None else premium_amount

        return round(final_premium), ""
    except Exception as e:
        return None, f"Ошибка при расчете премии: {str(e)}"

def calculate_quarterly_premium(final_premium):
    quarterly_premium = final_premium * values.COEFF_QUARTERLY_PAYMENT
    return round(quarterly_premium)