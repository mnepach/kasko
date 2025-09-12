import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.custom_filters import StateFilter
from telebot.storage import StateMemoryStorage
from datetime import datetime
from . import calculations as calc
from . import program as kasko_program
from ..res import strings as strings
from ..res import values as values

user_data = {}

class BotState(StatesGroup):
    ASK_VEHICLE_YEAR = State()
    ASK_IS_NEW_VEHICLE = State()
    ASK_VEHICLE_PRICE = State()
    ASK_IS_IN_LIST = State()
    ASK_VEHICLE_MAKE = State()
    ASK_IS_MULTIDRIVE = State()
    ASK_DRIVER_AGE = State()
    ASK_DRIVER_EXP = State()
    ASK_TERRITORY = State()
    ASK_IS_CREDIT_LEASING_PLEDGE = State()
    ASK_IS_LICENSED_PARTS = State()
    ASK_QUARTERLY_PAYMENT = State()

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, state_storage=StateMemoryStorage())
        self.bot.add_custom_filter(StateFilter(self.bot))
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['help'])(self.send_help)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_IS_NEW_VEHICLE)(self.handle_is_new_vehicle)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_IS_IN_LIST)(self.handle_is_in_list)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_TERRITORY)(self.handle_territory)
        self.bot.message_handler(state=BotState.ASK_IS_CREDIT_LEASING_PLEDGE)(self.handle_is_credit_leasing_pledge)
        self.bot.message_handler(state=BotState.ASK_IS_LICENSED_PARTS)(self.handle_is_licensed_parts)
        self.bot.message_handler(state=BotState.ASK_QUARTERLY_PAYMENT)(self.handle_quarterly_payment)

    def send_welcome(self, message):
        chat_id = message.chat.id
        user_data[chat_id] = {}
        user_data[chat_id]["insurance_variant"] = "А"
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE)
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR, reply_markup=types.ReplyKeyboardRemove())
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def send_help(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.HELP_MESSAGE)

    def is_valid_year(self, year_str):
        try:
            year = int(year_str)
            current_year = datetime.now().year
            max_vehicle_age = 13
            min_allowed_year = current_year - max_vehicle_age
            return min_allowed_year <= year <= current_year
        except ValueError:
            return False

    def is_valid_price(self, price_str):
        try:
            price = float(price_str)
            max_price = 30000000
            return 0 < price <= max_price
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

    def handle_vehicle_year(self, message):
        chat_id = message.chat.id
        year_str = message.text

        if self.is_valid_year(year_str):
            year = int(year_str)
            user_data[chat_id]["vehicle_year"] = year
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.NEW_VEHICLE_BUTTON), types.KeyboardButton(strings.USED_VEHICLE_BUTTON))
            self.bot.send_message(chat_id, strings.ASK_IS_NEW_VEHICLE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_NEW_VEHICLE)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def handle_is_new_vehicle(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.NEW_VEHICLE_BUTTON, strings.USED_VEHICLE_BUTTON]:
            user_data[chat_id]["is_new_vehicle"] = (response == strings.NEW_VEHICLE_BUTTON)
            age = calc.define_age(
                manufacture_year=user_data[chat_id]["vehicle_year"],
                is_new_vehicle=user_data[chat_id]["is_new_vehicle"]
            )
            if age is None:
                self.bot.send_message(chat_id, strings.INVALID_INPUT)
                self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)
                return
            user_data[chat_id]["vehicle_age_years"] = age
            if age > 7:
                user_data[chat_id]["insurance_variant"] = "Б"
            self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.NEW_VEHICLE_BUTTON), types.KeyboardButton(strings.USED_VEHICLE_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_price(self, message):
        chat_id = message.chat.id
        price_str = message.text

        if self.is_valid_price(price_str):
            price = float(price_str)
            user_data[chat_id]["vehicle_price_usd"] = price
            user_data[chat_id]["vehicle_price_full"] = price
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.ASK_IS_IN_LIST, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_IN_LIST)
        else:
            self.bot.send_message(chat_id, f"{strings.INVALID_INPUT} Страховая сумма должна быть от 1 до 30,000,000 USD.")
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)

    def handle_is_in_list(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_in_list"] = (response == strings.YES_BUTTON)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Geely"), types.KeyboardButton("Иная марка"))
            self.bot.send_message(chat_id, strings.ASK_VEHICLE_MAKE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_make(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in ["Geely", "Иная марка"]:
            user_data[chat_id]["vehicle_make"] = response
            user_data[chat_id]["is_geely"] = response == "Geely"
            user_data[chat_id]["make_coefficient"] = values.MAKE_COEFFICIENTS.get(response.upper(), 0.8)
            if user_data[chat_id]["is_geely"]:
                user_data[chat_id]["is_multidrive"] = True
                user_data[chat_id]["drivers_known"] = True
                user_data[chat_id]["num_drivers"] = 1
                user_data[chat_id]["drivers_data"] = []
                self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE, reply_markup=types.ReplyKeyboardRemove())
                self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
                self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
                self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Geely"), types.KeyboardButton("Иная марка"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_multidrive(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["is_multidrive"] = (response == strings.YES_BUTTON)
            user_data[chat_id]["drivers_known"] = user_data[chat_id]["is_multidrive"]
            user_data[chat_id]["num_drivers"] = 1
            user_data[chat_id]["drivers_data"] = []
            self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_driver_age(self, message):
        chat_id = message.chat.id
        response = message.text

        if self.is_valid_driver_age(response):
            age = int(response)
            user_data[chat_id]["drivers_data"] = [{"age": age, "experience": 0}]
            self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)
        else:
            self.bot.send_message(chat_id, "Возраст водителя должен быть от 16 до 80 лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)

    def handle_driver_exp(self, message):
        chat_id = message.chat.id
        response = message.text
        max_exp = user_data[chat_id]["drivers_data"][0]["age"] - 16

        if self.is_valid_driver_exp(response, max_exp):
            exp = int(response)
            user_data[chat_id]["drivers_data"][0]["experience"] = exp
            user_data[chat_id]["multidrive_2_plus_years_exp"] = exp >= 2
            if user_data[chat_id]["is_geely"] and exp < 2:
                user_data[chat_id]["geely_low_exp_coeff"] = values.COEFF_GEELY_LOW_EXP
            else:
                user_data[chat_id]["geely_low_exp_coeff"] = 1.0
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Республика Беларусь"), types.KeyboardButton("Республика Беларусь и за ее пределами"))
            self.bot.send_message(chat_id, strings.ASK_TERRITORY, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_TERRITORY)
        else:
            self.bot.send_message(chat_id, f"Стаж вождения не может превышать {max_exp} лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def handle_territory(self, message):
        chat_id = message.chat.id
        territory = message.text

        if territory in ["Республика Беларусь", "Республика Беларусь и за ее пределами"]:
            user_data[chat_id]["territory"] = territory
            if user_data[chat_id]["is_geely"]:
                user_data[chat_id]["credit_leasing_pledge"] = False
                self.proceed_to_licensed_parts_or_calc(chat_id)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
                self.bot.send_message(chat_id, strings.ASK_IS_CREDIT_LEASING_PLEDGE, reply_markup=markup)
                self.bot.set_state(chat_id, BotState.ASK_IS_CREDIT_LEASING_PLEDGE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("Республика Беларусь"), types.KeyboardButton("Республика Беларусь и за ее пределами"))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_credit_leasing_pledge(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["credit_leasing_pledge"] = (response == strings.YES_BUTTON)
            self.proceed_to_licensed_parts_or_calc(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def proceed_to_licensed_parts_or_calc(self, chat_id):
        if user_data[chat_id]["insurance_variant"] == "А":
            if user_data[chat_id]["vehicle_age_years"] < 3:
                self.bot.send_message(chat_id, strings.CANT_CALCULATE_NEW_CAR, reply_markup=types.ReplyKeyboardRemove())
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
                return
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.ASK_IS_LICENSED_PARTS, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_LICENSED_PARTS)
        else:
            user_data[chat_id]["licensed_parts"] = False
            self.calculate_and_send_premium_from_state(chat_id)

    def handle_is_licensed_parts(self, message):
        chat_id = message.chat.id
        response = message.text

        if response in [strings.YES_BUTTON, strings.NO_BUTTON]:
            user_data[chat_id]["licensed_parts"] = (response == strings.YES_BUTTON)
            self.calculate_and_send_premium_from_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def calculate_and_send_premium_from_state(self, chat_id):
        dummy_message = type('obj', (object,), {'chat': type('obj', (object,), {'id': chat_id})})()
        self.calculate_and_send_premium(dummy_message)

    def handle_quarterly_payment(self, message):
        chat_id = message.chat.id
        response = message.text
        user_data[chat_id]["quarterly_payment"] = (response == strings.YES_BUTTON)

        if response == strings.YES_BUTTON:
            try:
                data = user_data[chat_id]
                response_message = f"Предварительный расчет страховой премии при ежеквартальной оплате (Вариант {data['insurance_variant']}):\n\n"
                has_results = False
                error_messages = []

                for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
                    calculation_data = {
                        "program": program_name,
                        "variant": data["insurance_variant"],
                        "vehicle_age_years": data["vehicle_age_years"],
                        "vehicle_price_usd": data["vehicle_price_usd"],
                        "vehicle_price_full": data["vehicle_price_full"],
                        "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
                        "drivers_known": data["drivers_known"],
                        "num_drivers": data["num_drivers"],
                        "drivers_data": data.get("drivers_data", []),
                        "is_geely": data.get("is_geely", False),
                        "territory": data.get("territory"),
                        "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                        "licensed_parts": data.get("licensed_parts", False),
                        "multidrive_2_plus_years_exp": data.get("multidrive_2_plus_years_exp", False),
                        "is_in_list": data.get("is_in_list", False),
                        "quarterly_payment": data.get("quarterly_payment", False),
                        "geely_low_exp_coeff": data.get("geely_low_exp_coeff", 1.0)
                    }

                    final_premium, error_message = calc.calculate_final_premium(calculation_data)
                    if final_premium is not None:
                        quarterly_premium = calc.calculate_quarterly_premium(final_premium)
                        quarterly_premium = round(quarterly_premium * data.get("make_coefficient", 0.8))
                        response_message += f"{program_name}: {quarterly_premium} USD\n"
                        has_results = True
                    else:
                        error_messages.append(f"{program_name}: {error_message}")

                if has_results:
                    response_message += "\nДля точного расчета обратитесь в страховую компанию."
                    if error_messages:
                        response_message += "\n\nНе рассчитаны следующие программы:\n" + "\n".join(error_messages)
                else:
                    response_message = strings.CALCULATION_ERROR.format("\n\nПричины:\n" + "\n".join(error_messages))

                self.bot.send_message(chat_id, response_message, reply_markup=types.ReplyKeyboardRemove())
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
            except Exception as e:
                print(f"Error in handle_quarterly_payment: {str(e)}")
                self.bot.send_message(chat_id, strings.CALCULATION_ERROR.format(str(e)), reply_markup=types.ReplyKeyboardRemove())
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
        elif response == strings.NO_BUTTON:
            self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
            self.bot.delete_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def calculate_and_send_premium(self, message):
        chat_id = message.chat.id
        try:
            data = user_data[chat_id]
            response_message = f"Предварительный расчет страховой премии (Вариант {data['insurance_variant']}):\n\n"
            has_results = False
            error_messages = []

            for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
                calculation_data = {
                    "program": program_name,
                    "variant": data["insurance_variant"],
                    "vehicle_age_years": data["vehicle_age_years"],
                    "vehicle_price_usd": data["vehicle_price_usd"],
                    "vehicle_price_full": data["vehicle_price_full"],
                    "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
                    "drivers_known": data["drivers_known"],
                    "num_drivers": data["num_drivers"],
                    "drivers_data": data.get("drivers_data", []),
                    "is_geely": data.get("is_geely", False),
                    "territory": data.get("territory"),
                    "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                    "licensed_parts": data.get("licensed_parts", False),
                    "multidrive_2_plus_years_exp": data.get("multidrive_2_plus_years_exp", False),
                    "is_in_list": data.get("is_in_list", False),
                    "quarterly_payment": data.get("quarterly_payment", False),
                    "geely_low_exp_coeff": data.get("geely_low_exp_coeff", 1.0)
                }

                final_premium, error_message = calc.calculate_final_premium(calculation_data)
                if final_premium is not None:
                    final_premium = round(final_premium * data.get("make_coefficient", 0.8))
                    response_message += f"{program_name}: {final_premium} USD\n"
                    has_results = True
                else:
                    error_messages.append(f"{program_name}: {error_message}")

            if has_results:
                response_message += "\nДля точного расчета обратитесь в страховую компанию."
                if error_messages:
                    response_message += "\n\nНе рассчитаны следующие программы:\n" + "\n".join(error_messages)
            else:
                response_message = strings.CALCULATION_ERROR.format("\n\nПричины:\n" + "\n".join(error_messages))

            self.bot.send_message(chat_id, response_message, reply_markup=types.ReplyKeyboardRemove())
            self.ask_quarterly_payment(message)
        except Exception as e:
            print(f"Error in calculate_and_send_premium: {str(e)}")
            self.bot.send_message(chat_id, strings.CALCULATION_ERROR.format(str(e)))
            self.ask_quarterly_payment(message)

    def ask_quarterly_payment(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(strings.YES_BUTTON), types.KeyboardButton(strings.NO_BUTTON))
        self.bot.send_message(chat_id, strings.ASK_QUARTERLY_PAYMENT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_QUARTERLY_PAYMENT)

    def run(self):
        print("Bot started...")
        self.bot.infinity_polling()