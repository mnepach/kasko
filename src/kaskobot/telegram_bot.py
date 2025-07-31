import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.custom_filters import StateFilter
from datetime import datetime
from . import calculations as calc
from . import program as kasko_program
from ..res import strings as strings
from ..res import values as values

user_data = {}

class BotState(StatesGroup):
    SELECT_PROGRAM = State()
    ASK_IS_RENEWAL = State()
    ASK_IS_NEW_VEHICLE = State()
    ASK_REGISTRATION_DATE = State()
    ASK_VEHICLE_YEAR = State()
    ASK_VEHICLE_PRICE = State()
    ASK_IS_FULL_INSURANCE = State()
    ASK_INSURANCE_AMOUNT = State()  # Новое состояние для страховой суммы
    ASK_INSURANCE_VARIANT = State()
    ASK_CLIENT_TYPE = State()
    ASK_IS_MULTIDRIVE = State()
    ASK_NUM_DRIVERS = State()
    ASK_DRIVER_AGE = State()
    ASK_DRIVER_EXP = State()
    ASK_VEHICLE_MAKE = State()
    ASK_VEHICLE_MAKE_OTHER = State()
    ASK_TERRITORY = State()
    ASK_CALC_ONLY_BY_ESTIMATION = State()
    ASK_IS_CREDIT_LEASING_PLEDGE = State()
    ASK_HAS_ADDITIONAL_OPTIONS = State()
    ASK_IS_TAXI_UBER = State()
    ASK_IS_EMPLOYEE_CORP = State()
    ASK_HAS_SATELLITE_ALARM = State()
    ASK_HAS_MARKING = State()
    ASK_IS_SINGLE_PAYMENT = State()
    ASK_IS_LICENSED_PARTS = State()
    ASK_HAS_WHEEL_DISKS_RISK = State()
    ASK_TRANSIT_TERM = State()
    ASK_NUM_VEHICLES_INSURED = State()
    ASK_IS_FAMILY = State()
    ASK_HAS_OTHER_INSURANCE = State()
    ASK_OTHER_INSURANCE_AMOUNT = State()
    ASK_BONUS_CLASS = State()
    ASK_CLAIMS_COUNT = State()
    ASK_HAS_ADDITIONAL_EQUIPMENT = State()
    ASK_ADDITIONAL_EQUIPMENT_DETAILS = State()
    CALCULATE_PREMIUM = State()

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.add_custom_filter(StateFilter(self.bot))
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(state=BotState.SELECT_PROGRAM)(self.handle_program_selection)
        self.bot.message_handler(state=BotState.ASK_IS_RENEWAL)(self.handle_is_renewal)
        self.bot.message_handler(state=BotState.ASK_IS_NEW_VEHICLE)(self.handle_is_new_vehicle)
        self.bot.message_handler(state=BotState.ASK_REGISTRATION_DATE)(self.handle_registration_date)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_IS_FULL_INSURANCE)(self.handle_is_full_insurance)
        self.bot.message_handler(state=BotState.ASK_INSURANCE_AMOUNT)(self.handle_insurance_amount)
        self.bot.message_handler(state=BotState.ASK_INSURANCE_VARIANT)(self.handle_insurance_variant)
        self.bot.message_handler(state=BotState.ASK_CLIENT_TYPE)(self.handle_client_type)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_NUM_DRIVERS)(self.handle_num_drivers)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE_OTHER)(self.handle_vehicle_make_other)
        self.bot.message_handler(state=BotState.ASK_TERRITORY)(self.handle_territory)
        self.bot.message_handler(state=BotState.ASK_CALC_ONLY_BY_ESTIMATION)(self.handle_calc_only_by_estimation)
        self.bot.message_handler(state=BotState.ASK_IS_CREDIT_LEASING_PLEDGE)(self.handle_is_credit_leasing_pledge)
        self.bot.message_handler(state=BotState.ASK_HAS_ADDITIONAL_OPTIONS)(self.handle_has_additional_options)
        self.bot.message_handler(state=BotState.ASK_IS_TAXI_UBER)(self.handle_is_taxi_uber)
        self.bot.message_handler(state=BotState.ASK_IS_EMPLOYEE_CORP)(self.handle_is_employee_corp)
        self.bot.message_handler(state=BotState.ASK_HAS_SATELLITE_ALARM)(self.handle_has_satellite_alarm)
        self.bot.message_handler(state=BotState.ASK_HAS_MARKING)(self.handle_has_marking)
        self.bot.message_handler(state=BotState.ASK_IS_SINGLE_PAYMENT)(self.handle_is_single_payment)
        self.bot.message_handler(state=BotState.ASK_IS_LICENSED_PARTS)(self.handle_is_licensed_parts)
        self.bot.message_handler(state=BotState.ASK_HAS_WHEEL_DISKS_RISK)(self.handle_has_wheel_disks_risk)
        self.bot.message_handler(state=BotState.ASK_TRANSIT_TERM)(self.handle_transit_term)
        self.bot.message_handler(state=BotState.ASK_NUM_VEHICLES_INSURED)(self.handle_num_vehicles_insured)
        self.bot.message_handler(state=BotState.ASK_IS_FAMILY)(self.handle_is_family)
        self.bot.message_handler(state=BotState.ASK_HAS_OTHER_INSURANCE)(self.handle_has_other_insurance)
        self.bot.message_handler(state=BotState.ASK_OTHER_INSURANCE_AMOUNT)(self.handle_other_insurance_amount)
        self.bot.message_handler(state=BotState.ASK_BONUS_CLASS)(self.handle_bonus_class)
        self.bot.message_handler(state=BotState.ASK_CLAIMS_COUNT)(self.handle_claims_count)
        self.bot.message_handler(state=BotState.ASK_HAS_ADDITIONAL_EQUIPMENT)(self.handle_has_additional_equipment)
        self.bot.message_handler(state=BotState.ASK_ADDITIONAL_EQUIPMENT_DETAILS)(self.handle_additional_equipment_details)

    def run(self):
        print("Bot started...")
        self.bot.infinity_polling()

    def send_welcome(self, message):
        chat_id = message.chat.id
        user_data[chat_id] = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
            markup.add(types.KeyboardButton(program_name))
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.SELECT_PROGRAM)

    def is_valid_year(self, year_str):
        try:
            year = int(year_str)
            current_year = datetime.now().year
            return 1900 <= year <= current_year
        except ValueError:
            return False

    def is_valid_price(self, price_str):
        try:
            price = float(price_str)
            return price > 0
        except ValueError:
            return False

    def is_valid_driver_age(self, age_str):
        try:
            age = int(age_str)
            return 16 <= age <= 80
        except ValueError:
            return False

    def is_valid_driver_exp(self, exp_str, max_exp):
        try:
            exp = int(exp_str)
            return 0 <= exp <= max_exp
        except ValueError:
            return False

    def is_valid_transit_term(self, term_str):
        try:
            term = int(term_str)
            return 1 <= term <= 30
        except ValueError:
            return False

    def is_valid_num_vehicles(self, num_str):
        try:
            num = int(num_str)
            return num >= 1
        except ValueError:
            return False

    def is_valid_insurance_amount(self, amount_str):
        try:
            amount = float(amount_str)
            return amount >= 0
        except ValueError:
            return False

    def is_valid_claims_count(self, count_str):
        try:
            count = int(count_str)
            return count >= 0
        except ValueError:
            return False

    def ask_is_renewal(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_RENEWAL, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_RENEWAL)

    def ask_is_new_vehicle(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_NEW_VEHICLE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_NEW_VEHICLE)

    def ask_registration_date(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_REGISTRATION_DATE, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_REGISTRATION_DATE)

    def ask_vehicle_year(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def ask_vehicle_price(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)

    def ask_is_full_insurance(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_FULL_INSURANCE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_FULL_INSURANCE)

    def ask_insurance_amount(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Введите страховую сумму ТС в USD:", reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_INSURANCE_AMOUNT)

    def ask_insurance_variant(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Вариант А"), types.KeyboardButton("Вариант Б"))
        self.bot.send_message(chat_id, strings.ASK_INSURANCE_VARIANT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_INSURANCE_VARIANT)

    def ask_client_type(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Физическое лицо"), types.KeyboardButton("ИП"), types.KeyboardButton("Юридическое лицо"))
        self.bot.send_message(chat_id, strings.ASK_CLIENT_TYPE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_CLIENT_TYPE)

    def ask_is_multidrive(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)

    def ask_num_drivers(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if user_data[chat_id]["is_multidrive"]:
            markup.add(types.KeyboardButton("1"))  # Только один водитель при мультивождении
        else:
            for i in range(2, 6):  # От 2 до 5 водителей при не мультивождении
                markup.add(types.KeyboardButton(str(i)))
        self.bot.send_message(chat_id, strings.ASK_NUM_DRIVERS, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_NUM_DRIVERS)

    def ask_driver_age(self, message, driver_index):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE.format(driver_index + 1), reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)

    def ask_driver_exp(self, message, driver_index):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP.format(driver_index + 1), reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def ask_vehicle_make(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("BMW"), types.KeyboardButton("Geely"), types.KeyboardButton("Иная марка"))
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_MAKE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE)

    def ask_vehicle_make_other(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Пожалуйста, введите марку автомобиля:", reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE_OTHER)

    def ask_territory(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Республика Беларусь"), types.KeyboardButton("Республика Беларусь и за ее пределами"))
        self.bot.send_message(chat_id, strings.ASK_TERRITORY, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_TERRITORY)

    def ask_calc_only_by_estimation(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_CALC_ONLY_BY_ESTIMATION, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_CALC_ONLY_BY_ESTIMATION)

    def ask_is_credit_leasing_pledge(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_CREDIT_LEASING_PLEDGE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_CREDIT_LEASING_PLEDGE)

    def ask_has_additional_options(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_ADDITIONAL_OPTIONS, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_ADDITIONAL_OPTIONS)

    def ask_is_taxi_uber(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_TAXI_UBER, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_TAXI_UBER)

    def ask_is_employee_corp(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_EMPLOYEE_CORP, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_EMPLOYEE_CORP)

    def ask_has_satellite_alarm(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_SATELLITE_ALARM, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_SATELLITE_ALARM)

    def ask_has_marking(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_MARKING, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_MARKING)

    def ask_is_single_payment(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_SINGLE_PAYMENT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_SINGLE_PAYMENT)

    def ask_is_licensed_parts(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_LICENSED_PARTS, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_LICENSED_PARTS)

    def ask_has_wheel_disks_risk(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_WHEEL_DISKS_RISK, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_WHEEL_DISKS_RISK)

    def ask_transit_term(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("До 7 дней"), types.KeyboardButton("8–14 дней"), types.KeyboardButton("15–30 дней"))
        self.bot.send_message(chat_id, strings.ASK_TRANSIT_TERM, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_TRANSIT_TERM)

    def ask_num_vehicles_insured(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_NUM_VEHICLES_INSURED, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_NUM_VEHICLES_INSURED)

    def ask_is_family(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_FAMILY, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_FAMILY)

    def ask_has_other_insurance(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_OTHER_INSURANCE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_OTHER_INSURANCE)

    def ask_other_insurance_amount(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_OTHER_INSURANCE_AMOUNT, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_OTHER_INSURANCE_AMOUNT)

    def ask_bonus_class(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for bonus_class in ["С0", "С1", "С2", "С3"]:
            markup.add(types.KeyboardButton(bonus_class))
        self.bot.send_message(chat_id, strings.ASK_BONUS_CLASS, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_BONUS_CLASS)

    def ask_claims_count(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_CLAIMS_COUNT, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_CLAIMS_COUNT)

    def ask_has_additional_equipment(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_HAS_ADDITIONAL_EQUIPMENT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_HAS_ADDITIONAL_EQUIPMENT)

    def ask_additional_equipment_details(self, message):
        chat_id = message.chat.id
        self.bot.send_message(
            chat_id,
            "Укажите перечень и стоимость дополнительного оборудования в USD (например, 'Аудиосистема, 1000'). Если оборудования нет, введите 'Нет':",
            reply_markup=types.ReplyKeyboardRemove()
        )
        self.bot.set_state(chat_id, BotState.ASK_ADDITIONAL_EQUIPMENT_DETAILS)

    def handle_program_selection(self, message):
        chat_id = message.chat.id
        program_name = message.text

        if program_name in kasko_program.AVAILABLE_PROGRAMS:
            user_data[chat_id]["program"] = kasko_program.AVAILABLE_PROGRAMS[program_name]
            user_data[chat_id]["program_name"] = program_name
            self.ask_is_renewal(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.send_welcome(message)

    def handle_is_renewal(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_renewal"] = (response == strings.YES_BUTTON)
            self.ask_is_new_vehicle(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_new_vehicle(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_new_vehicle"] = (response == strings.YES_BUTTON)
            if user_data[chat_id]["is_new_vehicle"]:
                self.ask_registration_date(message)
            else:
                self.ask_vehicle_year(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_registration_date(self, message):
        chat_id = message.chat.id
        reg_date = message.text

        try:
            datetime.strptime(reg_date, '%d.%m.%Y')
            user_data[chat_id]["registration_date"] = reg_date
            self.ask_vehicle_year(message)
        except ValueError:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_registration_date(message)

    def handle_vehicle_year(self, message):
        chat_id = message.chat.id
        year_str = message.text

        if self.is_valid_year(year_str):
            year = int(year_str)
            user_data[chat_id]["vehicle_year"] = year
            age = calc.define_age(
                manufacture_year=year,
                is_renewal=user_data[chat_id].get("is_renewal", False),
                is_new_vehicle=user_data[chat_id].get("is_new_vehicle", False),
                registration_date=user_data[chat_id].get("registration_date", None)
            )
            if age is None or age > 13:
                self.bot.send_message(chat_id, strings.CONTACT_MANAGER)
                self.send_welcome(message)
                return
            user_data[chat_id]["vehicle_age_years"] = age
            self.ask_vehicle_price(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_vehicle_year(message)

    def handle_vehicle_price(self, message):
        chat_id = message.chat.id
        price_str = message.text

        if self.is_valid_price(price_str):
            price = float(price_str)
            user_data[chat_id]["vehicle_price_full"] = price
            user_data[chat_id]["vehicle_price"] = price  
            self.ask_is_full_insurance(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_vehicle_price(message)

    def handle_is_full_insurance(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_full_insurance"] = (response == strings.YES_BUTTON)
            if not user_data[chat_id]["is_full_insurance"]:
                self.ask_insurance_amount(message)
            else:
                if user_data[chat_id]["program_name"] == "Доброе КАСКО":
                    user_data[chat_id]["insurance_variant"] = "Вариант Б"
                    self.ask_client_type(message)
                else:
                    self.ask_insurance_variant(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_insurance_amount(self, message):
        chat_id = message.chat.id
        amount_str = message.text

        if self.is_valid_price(amount_str):
            amount = float(amount_str)
            user_data[chat_id]["vehicle_price"] = amount  
            if user_data[chat_id]["program_name"] == "Доброе КАСКО":
                user_data[chat_id]["insurance_variant"] = "Вариант Б"
                self.ask_client_type(message)
            else:
                self.ask_insurance_variant(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_insurance_amount(message)

    def handle_insurance_variant(self, message):
        chat_id = message.chat.id
        variant = message.text

        if variant in ["Вариант А", "Вариант Б"]:
            user_data[chat_id]["insurance_variant"] = variant
            program_name = user_data[chat_id]["program_name"]
            if program_name == "Доброе КАСКО" and variant == "Вариант А":
                self.bot.send_message(chat_id, strings.INVALID_INPUT)
                self.ask_insurance_variant(message)
                return
            if program_name != "КАСКО-Транзит" and variant == "Вариант А":
                self.ask_calc_only_by_estimation(message)
            elif program_name == "КАСКО-Транзит":
                user_data[chat_id]["is_calc_only_by_estimation"] = False
                self.ask_transit_term(message)
            else:
                user_data[chat_id]["is_calc_only_by_estimation"] = False
                self.ask_client_type(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Вариант А"), types.KeyboardButton("Вариант Б"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_transit_term(self, message):
        chat_id = message.chat.id
        term_str = message.text

        term_map = {
            "До 7 дней": 7,
            "8–14 дней": 14,
            "15–30 дней": 30
        }
        if term_str in term_map:
            user_data[chat_id]["transit_term_days"] = term_map[term_str]
            self.ask_client_type(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_transit_term(message)

    def handle_client_type(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in ["Физическое лицо", "ИП", "Юридическое лицо"]:
            user_data[chat_id]["client_type"] = {
                "Физическое лицо": "физ_лицо",
                "ИП": "ип",
                "Юридическое лицо": "юр_лицо"
            }[response]
            if user_data[chat_id]["client_type"] in ["ип", "юр_лицо"]:
                user_data[chat_id]["is_multidrive"] = True
                user_data[chat_id]["drivers_data"] = []
                user_data[chat_id]["num_drivers"] = None
                self.ask_vehicle_make(message)
            else:
                self.ask_is_multidrive(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Физическое лицо"), types.KeyboardButton("ИП"), types.KeyboardButton("Юридическое лицо"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_multidrive(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_multidrive"] = (response == strings.YES_BUTTON)
            user_data[chat_id]["drivers_data"] = []
            user_data[chat_id]["current_driver_index"] = 0
            if user_data[chat_id]["is_multidrive"]:
                user_data[chat_id]["num_drivers"] = 1  # Автоматически один водитель
                self.ask_driver_age(message, 0)
            else:
                self.ask_num_drivers(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_num_drivers(self, message):
        chat_id = message.chat.id
        num_str = message.text

        try:
            num_drivers = int(num_str)
            if user_data[chat_id]["is_multidrive"]:
                if num_drivers == 1:
                    user_data[chat_id]["num_drivers"] = num_drivers
                    user_data[chat_id]["drivers_data"] = []
                    user_data[chat_id]["current_driver_index"] = 0
                    self.ask_driver_age(message, 0)
                else:
                    self.bot.send_message(chat_id, "При мультивождении допускается только один водитель.")
                    self.ask_num_drivers(message)
            else:
                if 2 <= num_drivers <= 5:
                    user_data[chat_id]["num_drivers"] = num_drivers
                    user_data[chat_id]["drivers_data"] = []
                    user_data[chat_id]["current_driver_index"] = 0
                    self.ask_driver_age(message, 0)
                else:
                    self.bot.send_message(chat_id, "Количество водителей должно быть от 2 до 5.")
                    self.ask_num_drivers(message)
        except ValueError:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_num_drivers(message)

    def handle_driver_age(self, message):
        chat_id = message.chat.id
        age_str = message.text
        current_driver_index = user_data[chat_id]["current_driver_index"]

        if self.is_valid_driver_age(age_str):
            age = int(age_str)
            if current_driver_index >= len(user_data[chat_id]["drivers_data"]):
                user_data[chat_id]["drivers_data"].append({"age": age, "experience": 0})
            else:
                user_data[chat_id]["drivers_data"][current_driver_index]["age"] = age
            self.ask_driver_exp(message, current_driver_index)
        else:
            self.bot.send_message(chat_id, "Возраст водителя должен быть от 16 до 80 лет.")
            self.ask_driver_age(message, current_driver_index)

    def handle_driver_exp(self, message):
        chat_id = message.chat.id
        exp_str = message.text
        current_driver_index = user_data[chat_id]["current_driver_index"]
        num_drivers = user_data[chat_id]["num_drivers"]
        max_exp = user_data[chat_id]["drivers_data"][current_driver_index]["age"] - 16

        if self.is_valid_driver_exp(exp_str, max_exp):
            user_data[chat_id]["drivers_data"][current_driver_index]["experience"] = int(exp_str)
            user_data[chat_id]["current_driver_index"] += 1
            if user_data[chat_id]["current_driver_index"] < num_drivers:
                self.ask_driver_age(message, user_data[chat_id]["current_driver_index"])
            else:
                self.ask_vehicle_make(message)
        else:
            self.bot.send_message(chat_id, f"Стаж вождения не может превышать {max_exp} лет.")
            self.ask_driver_exp(message, current_driver_index)

    def handle_vehicle_make(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in ["BMW", "Geely", "Иная марка"]:
            if response == "Иная марка":
                self.ask_vehicle_make_other(message)
            else:
                user_data[chat_id]["vehicle_make"] = response
                self.ask_territory(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("BMW"), types.KeyboardButton("Geely"), types.KeyboardButton("Иная марка"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_make_other(self, message):
        chat_id = message.chat.id
        make = message.text.strip().upper()
        forbidden_makes = ["BENTLEY", "FERRARI", "ROLLS-ROYCE", "LAMBORGHINI", "MASERATI"]

        if make in forbidden_makes:
            self.bot.send_message(chat_id, strings.CONTACT_MANAGER)
            self.send_welcome(message)
        else:
            user_data[chat_id]["vehicle_make"] = make
            self.ask_territory(message)

    def handle_territory(self, message):
        chat_id = message.chat.id
        territory = message.text

        if territory in ["Республика Беларусь", "Республика Беларусь и за ее пределами"]:
            user_data[chat_id]["territory_option"] = territory
            self.ask_is_credit_leasing_pledge(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Республика Беларусь"), types.KeyboardButton("Республика Беларусь и за ее пределами"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_calc_only_by_estimation(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_calc_only_by_estimation"] = (response == strings.YES_BUTTON)
            self.ask_client_type(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_credit_leasing_pledge(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_credit_leasing_pledge"] = (response == strings.YES_BUTTON)
            self.ask_has_additional_options(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_additional_options(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_additional_options"] = (response == strings.YES_BUTTON)
            self.ask_is_taxi_uber(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_taxi_uber(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_taxi_uber"] = (response == strings.YES_BUTTON)
            self.ask_is_employee_corp(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_employee_corp(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_employee_corp"] = (response == strings.YES_BUTTON)
            self.ask_has_satellite_alarm(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_satellite_alarm(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_satellite_alarm"] = (response == strings.YES_BUTTON)
            self.ask_has_marking(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_marking(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_marking"] = (response == strings.YES_BUTTON)
            self.ask_is_single_payment(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_single_payment(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_single_payment"] = (response == strings.YES_BUTTON)
            program_name = user_data[chat_id]["program_name"]
            insurance_variant = user_data[chat_id]["insurance_variant"]
            vehicle_age_years = user_data[chat_id]["vehicle_age_years"]
            is_calc_only = user_data[chat_id].get("is_calc_only_by_estimation", False)

            if program_name not in ["КАСКО-Транзит", "Доброе КАСКО"] and insurance_variant == "Вариант А" and not is_calc_only and vehicle_age_years >= 3:
                self.ask_is_licensed_parts(message)
            else:
                user_data[chat_id]["is_licensed_parts"] = False
                if program_name == "КАСКО-Премиум":
                    self.ask_has_wheel_disks_risk(message)
                else:
                    self.ask_num_vehicles_insured(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_licensed_parts(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_licensed_parts"] = (response == strings.YES_BUTTON)
            if user_data[chat_id]["program_name"] == "КАСКО-Премиум":
                self.ask_has_wheel_disks_risk(message)
            else:
                self.ask_num_vehicles_insured(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_wheel_disks_risk(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_wheel_disks_risk"] = (response == strings.YES_BUTTON)
            self.ask_num_vehicles_insured(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_num_vehicles_insured(self, message):
        chat_id = message.chat.id
        num_str = message.text

        if self.is_valid_num_vehicles(num_str):
            num_vehicles = int(num_str)
            user_data[chat_id]["num_vehicles_insured"] = num_vehicles
            if num_vehicles >= 2:
                self.ask_is_family(message)
            else:
                user_data[chat_id]["is_family"] = False
                self.ask_has_other_insurance(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_num_vehicles_insured(message)

    def handle_is_family(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_family"] = (response == strings.YES_BUTTON)
            self.ask_has_other_insurance(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_other_insurance(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_other_insurance"] = (response == strings.YES_BUTTON)
            if user_data[chat_id]["has_other_insurance"]:
                self.ask_other_insurance_amount(message)
            else:
                user_data[chat_id]["other_insurance_amount"] = 0
                self.ask_bonus_class(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_other_insurance_amount(self, message):
        chat_id = message.chat.id
        amount_str = message.text

        if self.is_valid_insurance_amount(amount_str):
            user_data[chat_id]["other_insurance_amount"] = float(amount_str)
            self.ask_bonus_class(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_other_insurance_amount(message)

    def handle_bonus_class(self, message):
        chat_id = message.chat.id
        bonus_class = message.text

        if bonus_class in ["С0", "С1", "С2", "С3"]:
            user_data[chat_id]["bonus_class"] = bonus_class
            self.ask_claims_count(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for bonus_class in ["С0", "С1", "С2", "С3"]:
                markup.add(types.KeyboardButton(bonus_class))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_claims_count(self, message):
        chat_id = message.chat.id
        count_str = message.text

        if self.is_valid_claims_count(count_str):
            user_data[chat_id]["claims_count"] = int(count_str)
            self.ask_has_additional_equipment(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_claims_count(message)

    def handle_has_additional_equipment(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_additional_equipment"] = (response == strings.YES_BUTTON)
            if user_data[chat_id]["has_additional_equipment"]:
                self.ask_additional_equipment_details(message)
            else:
                user_data[chat_id]["additional_equipment_cost"] = 0
                self.calculate_and_send_premium(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_additional_equipment_details(self, message):
        chat_id = message.chat.id
        details = message.text.strip()

        if details.lower() == "нет" or not details:
            user_data[chat_id]["additional_equipment_cost"] = 0
            self.calculate_and_send_premium(message)
        else:
            try:
                cost = float(details.split(',')[-1].strip())
                if cost >= 0:
                    user_data[chat_id]["additional_equipment_cost"] = cost
                    self.calculate_and_send_premium(message)
                else:
                    self.bot.send_message(chat_id, strings.INVALID_INPUT)
                    self.ask_additional_equipment_details(message)
            except (ValueError, IndexError):
                self.bot.send_message(chat_id, strings.INVALID_INPUT)
                self.ask_additional_equipment_details(message)

    def calculate_and_send_premium(self, message):
        chat_id = message.chat.id
        try:
            data = user_data[chat_id]
            program_name = data["program_name"]
            transit_term_days = data.get("transit_term_days", None)
            if program_name == "КАСКО-Транзит" and transit_term_days is None:
                raise ValueError("Для программы КАСКО-Транзит необходимо указать срок.")

            vehicle_make = data.get("vehicle_make", "").upper()
            is_geely = vehicle_make in ["GEELY", "BELGEE"]
            is_bmw = vehicle_make == "BMW"
            vehicle_age_years = data["vehicle_age_years"]
            client_type = data.get("client_type", "физ_лицо")
            drivers_known = not data["is_multidrive"] and client_type not in ["ип", "юр_лицо"]
            multidrive_2_plus_years = False
            if data["is_multidrive"] and data.get("drivers_data") and data["drivers_data"]:
                multidrive_2_plus_years = all(driver["experience"] >= 2 for driver in data["drivers_data"])

            calculation_data = {
                "program": program_name,
                "variant": data["insurance_variant"].replace("Вариант ", ""),
                "vehicle_age_years": vehicle_age_years,
                "vehicle_price_usd": data["vehicle_price"],
                "vehicle_price_full": data["vehicle_price_full"],
                "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
                "drivers_known": drivers_known,
                "num_drivers": data.get("num_drivers"),
                "drivers_data": data.get("drivers_data", []),
                "is_geely": is_geely,
                "is_legal_entity_ip": client_type in ["ип", "юр_лицо"],
                "multidrive_2_plus_years_exp": multidrive_2_plus_years,
                "territory": data["territory_option"],
                "exceeding_claims_norm": data.get("claims_count", 0) > 2,
                "num_vehicles_insured": data.get("num_vehicles_insured"),
                "is_family": data.get("is_family", False),
                "bonus_class": data.get("bonus_class", "С0"),
                "claims_count": data.get("claims_count", 0),
                "calculation_only": data.get("is_calc_only_by_estimation", False),
                "has_other_insurance": data.get("has_other_insurance", False),
                "other_insurance_amount": data.get("other_insurance_amount", 0),
                "credit_leasing_pledge": data.get("is_credit_leasing_pledge", False),
                "additional_options": data.get("has_additional_options", False),
                "is_taxi_uber": data.get("is_taxi_uber", False),
                "is_employee": data.get("is_employee_corp", False),
                "satellite_alarm": data.get("has_satellite_alarm", False),
                "marking": data.get("has_marking", False),
                "single_payment": data.get("is_single_payment", False),
                "licensed_parts": data.get("is_licensed_parts", False),
                "wheel_disks": data.get("has_wheel_disks_risk", False),
                "transit_term_days": transit_term_days,
                "is_full_insurance": data.get("is_full_insurance", True),
                "has_additional_equipment": data.get("has_additional_equipment", False),
                "additional_equipment_cost": data.get("additional_equipment_cost", 0)
            }

            final_premium_usd = calc.calculate_final_premium(calculation_data)
            if final_premium_usd is None:
                self.bot.send_message(chat_id, strings.CALCULATION_ERROR)
                self.send_welcome(message)
                return

            # конвертация в BYN
            exchange_rate = 3.25
            final_premium_byn = final_premium_usd * exchange_rate

            response_message = (
                f"Предварительный расчет страховой премии:\n\n"
                f"Программа: {program_name} {data['insurance_variant']}\n"
                f"Марка ТС: {data['vehicle_make']}\n"
                f"Возраст ТС: {vehicle_age_years} лет\n"
                f"Стоимость ТС: {data['vehicle_price_full']:,} USD\n"
                f"Страховая сумма: {data['vehicle_price']:,} USD\n"
                f"Водители: {'Неограниченное число' if (data['is_multidrive'] and not data['drivers_data']) or client_type in ['ип', 'юр_лицо'] else f'{len(data['drivers_data'])}'}\n"
                f"Территория: {data['territory_option']}\n"
                f"Итоговая премия: **{final_premium_byn:,.2f} BYN**"
            )
            if is_bmw and vehicle_age_years >= 5:
                response_message += "\n\n*Примечание*: Для BMW старше 5 лет выплата по хищению зеркал ограничена."

            self.bot.send_message(chat_id, response_message, parse_mode="Markdown")
            self.bot.send_message(chat_id, strings.THANK_YOU)
            self.send_welcome(message)

        except ValueError as e:
            self.bot.send_message(chat_id, f"Ошибка данных: {e}. Пожалуйста, попробуйте снова.")
            print(f"ValueError for chat_id {chat_id}: {e}")
            self.send_welcome(message)
        except Exception as e:
            self.bot.send_message(chat_id, strings.CALCULATION_ERROR)
            print(f"Unexpected error for chat_id {chat_id}: {e}")
            self.send_welcome(message)