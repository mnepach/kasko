import telebot
from telebot import types
from telebot.custom_filters import StateFilter
from datetime import datetime
from . import calculations as calc
from . import program as kasko_program
from ..res import strings as strings
from ..res import values as values

user_data = {}

# --- cостояния бота ---
class BotState:
    SELECT_PROGRAM = "SELECT_PROGRAM"
    ASK_VEHICLE_TYPE = "ASK_VEHICLE_TYPE"
    ASK_VEHICLE_YEAR = "ASK_VEHICLE_YEAR"
    ASK_VEHICLE_PRICE = "ASK_VEHICLE_PRICE"
    ASK_INSURANCE_VARIANT = "ASK_INSURANCE_VARIANT"
    ASK_IS_MULTIDRIVE = "ASK_IS_MULTIDRIVE"
    ASK_NUM_DRIVERS = "ASK_NUM_DRIVERS"
    ASK_DRIVER_AGE = "ASK_DRIVER_AGE"
    ASK_DRIVER_EXP = "ASK_DRIVER_EXP"
    ASK_CLIENT_TYPE = "ASK_CLIENT_TYPE"
    ASK_VEHICLE_MAKE = "ASK_VEHICLE_MAKE"
    ASK_TERRITORY = "ASK_TERRITORY"
    ASK_CALC_ONLY_BY_ESTIMATION = "ASK_CALC_ONLY_BY_ESTIMATION"
    ASK_IS_CREDIT_LEASING_PLEDGE = "ASK_IS_CREDIT_LEASING_PLEDGE"
    ASK_HAS_ADDITIONAL_OPTIONS = "ASK_HAS_ADDITIONAL_OPTIONS"
    ASK_IS_TAXI_UBER = "ASK_IS_TAXI_UBER"
    ASK_IS_EMPLOYEE_CORP = "ASK_IS_EMPLOYEE_CORP"
    ASK_HAS_SATELLITE_ALARM = "ASK_HAS_SATELLITE_ALARM"
    ASK_HAS_MARKING = "ASK_HAS_MARKING"
    ASK_IS_SINGLE_PAYMENT = "ASK_IS_SINGLE_PAYMENT"
    ASK_IS_LICENSED_PARTS = "ASK_IS_LICENSED_PARTS"
    ASK_HAS_WHEEL_DISKS_RISK = "ASK_HAS_WHEEL_DISKS_RISK"
    ASK_TRANSIT_TERM = "ASK_TRANSIT_TERM"
    CALCULATE_PREMIUM = "CALCULATE_PREMIUM"

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.add_custom_filter(StateFilter(self.bot))
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)

        # регистрация хэндлеров для каждого состояния
        self.bot.message_handler(state=BotState.SELECT_PROGRAM)(self.handle_program_selection)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_TYPE)(self.handle_vehicle_type)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_INSURANCE_VARIANT)(self.handle_insurance_variant)
        self.bot.message_handler(state=BotState.ASK_TRANSIT_TERM)(self.handle_transit_term)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_NUM_DRIVERS)(self.handle_num_drivers)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_CLIENT_TYPE)(self.handle_client_type)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
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

    def run(self):
        print("Bot started...")
        self.bot.infinity_polling()

    # --- хэндлеры команд ---
    def send_welcome(self, message):
        chat_id = message.chat.id
        user_data[chat_id] = {} 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
            markup.add(types.KeyboardButton(program_name))
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE, reply_markup=markup)
        self.bot.send_message(chat_id, strings.SELECT_PROGRAM_PROMPT)
        self.bot.set_state(chat_id, BotState.SELECT_PROGRAM)

    # --- валидация ввода ---
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

    def is_valid_age_exp(self, val_str):
        try:
            val = int(val_str)
            return 0 <= val <= 100
        except ValueError:
            return False

    def is_valid_transit_term(self, term_str):
        try:
            term = int(term_str)
            return 1 <= term <= 31 
        except ValueError:
            return False

    # --- вспомогательные функции для перехода по состояниям ---
    def ask_vehicle_year(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def ask_vehicle_price(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, reply_markup=types.ReplyKeyboardRemove()) 
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)

    def ask_insurance_variant(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Вариант А"), types.KeyboardButton("Вариант Б"))
        self.bot.send_message(chat_id, strings.ASK_INSURANCE_VARIANT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_INSURANCE_VARIANT)

    def ask_is_multidrive(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)

    def ask_num_drivers(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"),
                   types.KeyboardButton("4"), types.KeyboardButton("5")) 
        self.bot.send_message(chat_id, strings.ASK_NUM_DRIVERS, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_NUM_DRIVERS)

    def ask_driver_age(self, message, driver_index):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE.format(driver_index + 1))
        self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)

    def ask_driver_exp(self, message, driver_index):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP.format(driver_index + 1))
        self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def ask_client_type(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Физическое лицо"), types.KeyboardButton("ИП"), types.KeyboardButton("Юридическое лицо"))
        self.bot.send_message(chat_id, strings.ASK_CLIENT_TYPE, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_CLIENT_TYPE)

    def ask_vehicle_make(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_MAKE)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE)

    def ask_territory(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("РБ"), types.KeyboardButton("РБ+За пределами"))
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
        self.bot.send_message(chat_id, strings.ASK_TRANSIT_TERM)
        self.bot.set_state(chat_id, BotState.ASK_TRANSIT_TERM)

    # --- логика обработки сообщений ---

    def handle_program_selection(self, message):
        chat_id = message.chat.id
        program_name = message.text

        if program_name in kasko_program.AVAILABLE_PROGRAMS:
            selected_program = kasko_program.AVAILABLE_PROGRAMS[program_name]
            user_data[chat_id]["program"] = selected_program
            user_data[chat_id]["program_name"] = program_name 
            user_data[chat_id]["is_truck_program"] = selected_program.is_truck_program()

            if user_data[chat_id]["is_truck_program"]:
                user_data[chat_id]["vehicle_type"] = "Грузовое ТС"
                self.ask_vehicle_year(message)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(types.KeyboardButton("Легковое ТС"), types.KeyboardButton("Грузовое ТС"))
                self.bot.send_message(chat_id, strings.ASK_VEHICLE_TYPE, reply_markup=markup)
                self.bot.set_state(chat_id, BotState.ASK_VEHICLE_TYPE)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.send_welcome(message)

    def handle_vehicle_type(self, message):
        chat_id = message.chat.id
        vehicle_type = message.text

        if vehicle_type in ["Легковое ТС", "Грузовое ТС"]:
            user_data[chat_id]["vehicle_type"] = vehicle_type
            user_data[chat_id]["is_truck_program"] = (vehicle_type == "Грузовое ТС")
            self.ask_vehicle_year(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Легковое ТС"), types.KeyboardButton("Грузовое ТС"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_year(self, message):
        chat_id = message.chat.id
        year_str = message.text

        if self.is_valid_year(year_str):
            user_data[chat_id]["vehicle_year"] = int(year_str)

            if user_data[chat_id]["program_name"] == "Доброе КАСКО":
                user_data[chat_id]["insurance_variant"] = "Вариант Б"
                user_data[chat_id]["is_calc_only_by_estimation"] = False 
                self.ask_is_multidrive(message) 
            else:
                self.ask_vehicle_price(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)

    def handle_vehicle_price(self, message):
        chat_id = message.chat.id
        price_str = message.text

        if self.is_valid_price(price_str):
            user_data[chat_id]["vehicle_price"] = float(price_str)
            self.ask_insurance_variant(message) 
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)

    def handle_insurance_variant(self, message):
        chat_id = message.chat.id
        variant = message.text

        if variant in ["Вариант А", "Вариант Б"]:
            user_data[chat_id]["insurance_variant"] = variant

            program_name = user_data[chat_id]["program_name"]
            is_truck_program = user_data[chat_id]["is_truck_program"]

            if program_name != "КАСКО-Транзит" and not is_truck_program and variant == "Вариант А":
                self.ask_calc_only_by_estimation(message)
            elif program_name == "КАСКО-Транзит":
                user_data[chat_id]["is_calc_only_by_estimation"] = False
                self.ask_transit_term(message)
            else: # Все остальные случаи
                user_data[chat_id]["is_calc_only_by_estimation"] = False
                self.ask_is_multidrive(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Вариант А"), types.KeyboardButton("Вариант Б"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_transit_term(self, message):
        chat_id = message.chat.id
        term_str = message.text

        if self.is_valid_transit_term(term_str):
            user_data[chat_id]["transit_term_days"] = int(term_str)
            self.ask_is_multidrive(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)

    def handle_is_multidrive(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_multidrive"] = (response == strings.YES_BUTTON)
            user_data[chat_id]["drivers_data"] = []
            user_data[chat_id]["current_driver_index"] = 0

            if user_data[chat_id]["is_multidrive"]:
                self.ask_num_drivers(message)
            else:
                user_data[chat_id]["num_drivers"] = 1
                if user_data[chat_id]["program_name"] not in ["КАСКО-Бизнес Оптима", "КАСКО-Бизнес Эконом", "КАСКО-Транзит"]:
                    self.ask_driver_age(message, 0)
                else:
                    self.ask_client_type(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_num_drivers(self, message):
        chat_id = message.chat.id
        num_str = message.text

        try:
            num_drivers = int(num_str)
            if 1 <= num_drivers <= 5: 
                user_data[chat_id]["num_drivers"] = num_drivers
                user_data[chat_id]["drivers_data"] = []
                user_data[chat_id]["current_driver_index"] = 0
                self.ask_driver_age(message, 0)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"),
                           types.KeyboardButton("4"), types.KeyboardButton("5"))
                self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)
        except ValueError:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"),
                       types.KeyboardButton("4"), types.KeyboardButton("5"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_driver_age(self, message):
        chat_id = message.chat.id
        age_str = message.text
        current_driver_index = user_data[chat_id]["current_driver_index"]

        if self.is_valid_age_exp(age_str):
            if current_driver_index >= len(user_data[chat_id]["drivers_data"]):
                user_data[chat_id]["drivers_data"].append({"age": int(age_str), "experience": 0})
            else:
                user_data[chat_id]["drivers_data"][current_driver_index]["age"] = int(age_str)

            self.ask_driver_exp(message, current_driver_index)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_driver_age(message, current_driver_index)

    def handle_driver_exp(self, message):
        chat_id = message.chat.id
        exp_str = message.text
        current_driver_index = user_data[chat_id]["current_driver_index"]
        num_drivers = user_data[chat_id]["num_drivers"]

        if self.is_valid_age_exp(exp_str):
            user_data[chat_id]["drivers_data"][current_driver_index]["experience"] = int(exp_str)
            user_data[chat_id]["current_driver_index"] += 1

            if user_data[chat_id]["current_driver_index"] < num_drivers:
                self.ask_driver_age(message, user_data[chat_id]["current_driver_index"])
            else:
                self.ask_client_type(message)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.ask_driver_exp(message, current_driver_index)

    def handle_client_type(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in ["Физическое лицо", "ИП", "Юридическое лицо"]:
            if response == "Физическое лицо":
                user_data[chat_id]["client_type"] = "физ_лицо"
            elif response == "ИП":
                user_data[chat_id]["client_type"] = "ип"
            else: # "Юридическое лицо"
                user_data[chat_id]["client_type"] = "юр_лицо"

            self.ask_vehicle_make(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Физическое лицо"), types.KeyboardButton("ИП"), types.KeyboardButton("Юридическое лицо"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_make(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["vehicle_make"] = message.text.strip()
        self.ask_territory(message)

    def handle_territory(self, message):
        chat_id = message.chat.id
        territory = message.text

        if territory in ["РБ", "РБ+За пределами"]:
            user_data[chat_id]["territory_option"] = territory
            self.ask_is_credit_leasing_pledge(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("РБ"), types.KeyboardButton("РБ+За пределами"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_calc_only_by_estimation(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_calc_only_by_estimation"] = (response == strings.YES_BUTTON)

            if user_data[chat_id]["program_name"] == "КАСКО-Транзит":
                self.ask_transit_term(message)
            else:
                self.ask_is_multidrive(message)
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

            # lогика для is_licensed_parts
            program_name = user_data[chat_id]["program_name"]
            insurance_variant = user_data[chat_id]["insurance_variant"]
            vehicle_year = user_data[chat_id]["vehicle_year"]
            is_calc_only_by_estimation = user_data[chat_id].get("is_calc_only_by_estimation", False)

            if (program_name != "КАСКО-Транзит" and program_name != "Доброе КАСКО" and 
                insurance_variant == "Вариант А" and
                not is_calc_only_by_estimation and
                calc.define_age(manufacture_year=vehicle_year) >= 3):
                self.ask_is_licensed_parts(message)
            else:
                user_data[chat_id]["is_licensed_parts"] = False 

                if program_name == "КАСКО-Премиум":
                    self.ask_has_wheel_disks_risk(message)
                else:
                    self.calculate_and_send_premium(message)
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
                self.calculate_and_send_premium(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_has_wheel_disks_risk(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["has_wheel_disks_risk"] = (response == strings.YES_BUTTON)
            self.calculate_and_send_premium(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def calculate_and_send_premium(self, message):
        chat_id = message.chat.id
        try:
            data = user_data[chat_id]
            program_object = data["program"] 
            program_name_str = program_object.get_name() 

            transit_term_days = data.get("transit_term_days", None)
            if program_name_str == "КАСКО-Транзит" and transit_term_days is None:
                raise ValueError("Для программы КАСКО-Транзит необходимо указать срок.")

            vehicle_type_group_mapped = None
            if data["vehicle_type"] == "Легковое ТС":
                vehicle_type_group_mapped = values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK
            elif data["vehicle_type"] == "Грузовое ТС":

                if data.get("truck_category") == "1.5-8t":
                    vehicle_type_group_mapped = values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL
                elif data.get("truck_category") == "over_8t":
                    vehicle_type_group_mapped = values.VEHICLE_TYPE_HEAVY_TRUCK_TRAILER
                else:
                    vehicle_type_group_mapped = values.VEHICLE_TYPE_MEDIUM_TRUCK_BUS_SPECIAL 

            vehicle_age_years = datetime.now().year - data["vehicle_year"]

            multidrive_2_plus_years_exp_status = False
            if data["is_multidrive"] and data.get("drivers_data") and data["drivers_data"] and data["drivers_data"][0].get("experience", 0) >= 2:
                multidrive_2_plus_years_exp_status = True

            is_geely_vehicle = "GEELY" in data.get("vehicle_make", "").upper()
            
            client_type = data.get("client_type", "физ_лицо")
            drivers_known_status = not data["is_multidrive"] and client_type not in ["ип", "юр_лицо"]

            calculation_data = {
                "program": program_name_str, 
                "variant": data["insurance_variant"].replace("Вариант ", ""), 
                "vehicle_age_years": vehicle_age_years,
                "vehicle_price_usd": data["vehicle_price"],
                "vehicle_type_group": vehicle_type_group_mapped,
                "truck_subtype": data.get("truck_subtype", None), 
                "drivers_known": drivers_known_status, 
                "num_drivers": data.get("num_drivers", None),
                "driver_age": data["drivers_data"][0]["age"] if data.get("drivers_data") and data["drivers_data"] and drivers_known_status else None,
                "driver_exp": data["drivers_data"][0]["experience"] if data.get("drivers_data") and data["drivers_data"] and drivers_known_status else None,
                "is_geely": is_geely_vehicle,
                "is_legal_entity_ip": client_type in ["ип", "юр_лицо"],
                "multidrive_2_plus_years_exp": multidrive_2_plus_years_exp_status,
                "territory": "Республика Беларусь" if data["territory_option"] == "РБ" else "Республика Беларусь и за ее пределами",
                "exceeding_claims_norm": data.get("exceeding_claims_norm", False),
                "num_vehicles_insured": data.get("num_vehicles_insured", None),
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
                "transit_term_days": transit_term_days 
            }

            final_premium_usd = calc.calculate_final_premium(calculation_data)

            if final_premium_usd is None:
                self.bot.send_message(chat_id, "Не удалось рассчитать премию. Проверьте введенные данные или обратитесь к администратору.")
                return

            response_message = (
                f"Предварительный расчет страховой премии:\n\n"
                f"Программа: {program_name_str} {data['insurance_variant']}\n"
                f"Стоимость ТС: {data['vehicle_price']:,} USD\n"
                f"Возраст ТС: {vehicle_age_years} лет\n"
                f"Водители: {'Неограниченное число' if data['is_multidrive'] else 'Известные'}\n"
                f"Территория: {data['territory_option']}\n"
                f"Итоговая премия: **{final_premium_usd:,} USD**"
            )
            self.bot.send_message(chat_id, response_message, parse_mode="Markdown")

        except ValueError as e:
            self.bot.send_message(chat_id, f"Ошибка данных: {e}. Пожалуйста, попробуйте снова.")
            print(f"ValueError for chat_id {chat_id}: {e}")
        except Exception as e:
            self.bot.send_message(chat_id, "Произошла непредвиденная ошибка при расчете. Пожалуйста, попробуйте снова или свяжитесь с поддержкой.")
            print(f"An unexpected error occurred during calculation for chat_id {chat_id}: {e}")