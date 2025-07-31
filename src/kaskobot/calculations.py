import math
from datetime import datetime, date

from src.res import values
from src.res import strings

def define_age(manufacture_year=None, is_renewal=False, is_new_vehicle=False, registration_date=None):
    """
    Определяет возраст автомобиля в полных годах с учетом продления и даты регистрации для новых ТС.

    Аргументы:
        manufacture_year (int, optional): Год выпуска автомобиля.
        is_renewal (bool): Является ли договор продлением.
        is_new_vehicle (bool): Является ли ТС новым и приобретенным в автосалоне.
        registration_date (str, optional): Дата регистрации в формате 'ДД.ММ.ГГГГ'.

    Возвращает:
        int: Возраст автомобиля в полных годах (максимум 13 лет). None при неверных данных.
    """
    current_date = date.today()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day

    if manufacture_year is None or not isinstance(manufacture_year, int):
        print(f"Ошибка: Год выпуска должен быть целым числом, получено {manufacture_year}.")
        return None

    if is_new_vehicle and registration_date:
        try:
            reg_date = datetime.strptime(registration_date, '%d.%m.%Y').date()
            if reg_date.year >= current_year - 1:
                age = current_year - reg_date.year
                if current_date.month < reg_date.month or (current_date.month == reg_date.month and current_date.day < reg_date.day):
                    age -= 1
                return max(0, min(age, 13))
        except ValueError:
            print(f"Ошибка: Неверный формат даты регистрации: {registration_date}. Ожидается 'ДД.ММ.ГГГГ'.")
            return None

    age = current_year - manufacture_year
    if current_date.month < 7:  # До 1 июля
        age -= 1
    if is_renewal:
        age += 1
    return max(0, min(age, 13))

def get_age_category(age_years, vehicle_type_group):
    if vehicle_type_group == values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK:
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
        elif age_years > 6:
            return "7 лет"
    return None

def get_price_category(price, program_name):
    if program_name == "Доброе КАСКО":
        if price <= values.VEHICLE_PRICE_LIMIT_2:
            return values.VEHICLE_PRICE_LIMIT_2
        elif price <= values.VEHICLE_PRICE_LIMIT_5:
            return values.VEHICLE_PRICE_LIMIT_5
        else:
            return values.VEHICLE_PRICE_LIMIT_6
    else:
        if price <= values.VEHICLE_PRICE_LIMIT_1:
            return values.VEHICLE_PRICE_LIMIT_1
        elif price <= values.VEHICLE_PRICE_LIMIT_2:
            return values.VEHICLE_PRICE_LIMIT_2
        elif price <= values.VEHICLE_PRICE_LIMIT_3:
            return values.VEHICLE_PRICE_LIMIT_3
        else:
            return values.VEHICLE_PRICE_LIMIT_4

def calculate_base_tariff(program_name, variant, vehicle_age_years, vehicle_price_usd, vehicle_type_group):
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
    elif variant == "Б":
        if program_name == "КАСКО-Оптима":
            tariff_table = values.OPTIMA_B_RATES
        elif program_name == "КАСКО-Профит":
            tariff_table = values.PROFIT_B_RATES
        elif program_name == "КАСКО-Автопрофи":
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

    if tariff_table is None:
        return None

    price_category = get_price_category(vehicle_price_usd, program_name)
    return tariff_table.get(age_category, tariff_table.get("all", {})).get(price_category)

def calculate_k_driver(drivers_known, num_drivers, drivers_data, is_geely, is_legal_entity_ip, multidrive_2_plus_years_exp):
    k_driver = 1.0
    if drivers_known:
        if num_drivers == 1:
            driver_age = drivers_data[0]["age"]
            driver_exp = drivers_data[0]["experience"]
            age_group = "16-24" if driver_age <= 24 else "25-34" if driver_age <= 34 else "35_plus"
            exp_group = "less_1_year" if driver_exp < 1 else "1_year" if driver_exp == 1 else "2_plus_years"
            k_driver = values.DRIVER_AGE_EXP_RATES.get(exp_group, {}).get(age_group, 1.0)
        else:
            k_driver = max(
                values.DRIVER_AGE_EXP_RATES[
                    "less_1_year" if d["experience"] < 1 else
                    "1_year" if d["experience"] == 1 else
                    "2_plus_years"
                ][
                    "16-24" if d["age"] <= 24 else
                    "25-34" if d["age"] <= 34 else
                    "35_plus"
                ]
                for d in drivers_data
            )
    else:
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
    k_territory = values.TERRITORY_RATE_ALL_TERRITORIES
    if territory_option == "Республика Беларусь":
        k_territory = values.TERRITORY_RATE_RB_ONLY
    return k_territory

def calculate_k_park(num_vehicles, is_family):
    k_park = values.PARK_COEFFS[1]
    if num_vehicles >= 15:
        k_park = values.PARK_COEFFS[15]
    elif num_vehicles >= 5:
        k_park = values.PARK_COEFFS[5]
    elif num_vehicles >= 2 and is_family:
        k_park = values.PARK_COEFFS[2]
    return k_park

def calculate_k_bonus(prev_bonus_class, claims_count):
    k_bonus = values.BONUS_SYSTEM_COEFFS.get(prev_bonus_class, 1.0)
    return k_bonus

def calculate_k_additional(has_other_insurance, other_insurance_amount, vehicle_price_usd, is_credit_leasing_pledge, is_geely, calculation_only_selected):
    k_additional = 1.0
    applied_additional_coeff = False

    if has_other_insurance:
        threshold_met = False
        for limit, threshold_amount in sorted(values.CROSSLING_THRESHOLDS.items()):
            if vehicle_price_usd <= limit or (limit == values.VEHICLE_PRICE_LIMIT_4 and vehicle_price_usd > limit):
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
        if threshold_met:
            k_additional = values.CROSSLING_COEFF
            applied_additional_coeff = True

    if not applied_additional_coeff and has_other_insurance:
        threshold_met = False
        for limit, threshold_amount in sorted(values.SPECIAL_DISCOUNT_THRESHOLDS.items()):
            if vehicle_price_usd <= limit or (limit == values.VEHICLE_PRICE_LIMIT_4 and vehicle_price_usd > limit):
                if other_insurance_amount >= threshold_amount:
                    threshold_met = True
                break
        if threshold_met:
            k_additional = values.SPECIAL_DISCOUNT_COEFF
            applied_additional_coeff = True

    if not applied_additional_coeff and is_credit_leasing_pledge and not is_geely:
        k_additional = values.COEFF_CREDIT_LEASING_PLEDGE
    return k_additional

def calculate_final_premium(data):
    program_name = data.get("program")
    variant = data.get("variant")
    vehicle_age_years = data.get("vehicle_age_years")
    vehicle_price_usd = data.get("vehicle_price_usd")
    vehicle_type_group = data.get("vehicle_type_group")

    base_tariff = calculate_base_tariff(program_name, variant, vehicle_age_years, vehicle_price_usd, vehicle_type_group)
    if base_tariff is None:
        return None

    total_tariff = base_tariff / 100

    k_driver = calculate_k_driver(
        data.get("drivers_known"),
        data.get("num_drivers"),
        data.get("drivers_data", []),
        data.get("is_geely"),
        data.get("is_legal_entity_ip"),
        data.get("multidrive_2_plus_years_exp")
    )
    total_tariff *= k_driver

    k_territory = calculate_k_territory(data.get("territory"), vehicle_type_group)
    total_tariff *= k_territory

    if data.get("exceeding_claims_norm"):
        total_tariff *= values.COEFF_EXCEEDING_CLAIMS_NORM

    if data.get("num_vehicles_insured") is not None:
        total_tariff *= calculate_k_park(data.get("num_vehicles_insured"), data.get("is_family"))

    if program_name not in ["Доброе КАСКО", "КАСКО-Транзит"]:
        total_tariff *= calculate_k_bonus(data.get("bonus_class"), data.get("claims_count"))

    if data.get("calculation_only") and variant == "А" and not data.get("licensed_parts"):
        total_tariff *= values.COEFF_CALCULATION_ONLY

    total_tariff *= calculate_k_additional(
        data.get("has_other_insurance"),
        data.get("other_insurance_amount"),
        vehicle_price_usd,
        data.get("credit_leasing_pledge"),
        data.get("is_geely"),
        data.get("calculation_only")
    )

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
    if data.get("single_payment") and program_name != "КАСКО-Транзит":
        total_tariff *= values.COEFF_SINGLE_PAYMENT
    if data.get("licensed_parts") and variant == "А" and vehicle_age_years >= 3 and not data.get("calculation_only"):
        total_tariff *= values.COEFF_LICENSED_PARTS

    if program_name == "КАСКО-Премиум" and data.get("wheel_disks"):
        if vehicle_price_usd <= values.VEHICLE_PRICE_LIMIT_7:
            total_tariff *= values.COEFF_WHEEL_DISKS_LT_70K
        else:
            total_tariff *= values.COEFF_WHEEL_DISKS_GT_70K

    if program_name == "КАСКО-Транзит":
        term_days = data.get("transit_term_days")
        if term_days <= 7:
            total_tariff *= values.SHORT_TERM_COEFFS[7]
        elif term_days <= 14:
            total_tariff *= values.SHORT_TERM_COEFFS[14]
        else:
            total_tariff *= values.SHORT_TERM_COEFFS[30]

    total_tariff = round(total_tariff, 4)

    premium_amount = vehicle_price_usd * total_tariff
    if data.get("has_additional_equipment"):
        equipment_cost = data.get("additional_equipment_cost", 0)
        premium_amount += equipment_cost * total_tariff

    if program_name == "КАСКО-Премиум":
        premium_amount += values.PREMIUM_ADD_SERVICES_COST

    if not data.get("is_full_insurance"):
        premium_amount *= vehicle_price_usd / data["vehicle_price_full"]

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
    has_wheel_disks = data.get("wheel_disks")
    transit_term_days = data.get("transit_term_days")

    if program_name in ["КАСКО-Оптима", "КАСКО-Профит"]:
        if (vehicle_age_years <= 3 and data.get("drivers_known") and
                data.get("drivers_data", [{}])[0].get("age", 0) >= 35 and
                data.get("drivers_data", [{}])[0].get("experience", 0) >= 2 and
                variant == "А" and
                (data.get("is_geely") and data.get("multidrive_2_plus_years_exp") or not data.get("is_geely"))):
            return values.MIN_PREMIUMS_PASSENGER[program_name]["А_SHORT_TERM"]
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-Автопрофи":
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-За полцены":
        return values.MIN_PREMIUMS_PASSENGER[program_name][variant]
    elif program_name == "КАСКО-за треть цены":
        return values.MIN_PREMIUMS_PASSENGER[program_name]
    elif program_name == "КАСКО-Премиум":
        return values.MIN_PREMIUMS_PASSENGER[program_name]["WITH_DISKS" if has_wheel_disks else "NO_DISKS"]
    elif program_name == "Доброе КАСКО":
        return values.MIN_PREMIUMS_PASSENGER[program_name]
    elif program_name == "КАСКО-Транзит":
        if transit_term_days <= 7:
            return values.MIN_PREMIUMS_PASSENGER[program_name][7]
        elif transit_term_days <= 14:
            return values.MIN_PREMIUMS_PASSENGER[program_name][14]
        else:
            return values.MIN_PREMIUMS_PASSENGER[program_name][30]
    return 0