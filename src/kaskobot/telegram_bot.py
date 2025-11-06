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
import re

user_data = {}

class BotState(StatesGroup):
    ASK_VEHICLE_YEAR = State()
    ASK_VEHICLE_PRICE = State()
    ASK_VEHICLE_MAKE = State()
    ASK_BMW_MODEL = State()
    ASK_IS_IN_LIST = State()
    ASK_IS_MULTIDRIVE = State()
    ASK_DRIVER_AGE = State()
    ASK_DRIVER_EXP = State()
    ASK_TERRITORY = State()
    ASK_IS_CREDIT_LEASING_PLEDGE = State()
    ASK_GREEN_PLATES = State()
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
        self.bot.message_handler(content_types=['sticker', 'animation', 'photo'])(self.handle_invalid_content)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
        self.bot.message_handler(state=BotState.ASK_BMW_MODEL)(self.handle_bmw_model)
        self.bot.message_handler(state=BotState.ASK_IS_IN_LIST)(self.handle_is_in_list)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_TERRITORY)(self.handle_territory)
        self.bot.message_handler(state=BotState.ASK_IS_CREDIT_LEASING_PLEDGE)(self.handle_is_credit_leasing_pledge)
        self.bot.message_handler(state=BotState.ASK_GREEN_PLATES)(self.handle_green_plates)
        self.bot.message_handler(state=BotState.ASK_IS_LICENSED_PARTS)(self.handle_is_licensed_parts)
        self.bot.message_handler(state=BotState.ASK_QUARTERLY_PAYMENT)(self.handle_quarterly_payment)
        self.bot.message_handler(content_types=['text'])(self.handle_unexpected_text)

    def send_welcome(self, message):
        chat_id = message.chat.id
        user_data[chat_id] = {}
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def send_help(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.HELP_MESSAGE)

    def handle_invalid_content(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Ошибка: отправка стикеров, GIF или фото не поддерживается. Пожалуйста, используйте текстовый ввод.")

    def handle_unexpected_text(self, message):
        chat_id = message.chat.id
        if not self.bot.get_state(chat_id):
            self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())

    def is_valid_year(self, year_str):
        try:
            year = int(year_str)
            current_year = datetime.now().year
            max_vehicle_age = 7
            min_allowed_year = current_year - max_vehicle_age
            return min_allowed_year <= year <= current_year, year >= min_allowed_year
        except ValueError:
            return False, False

    def is_valid_price(self, price_str):
        try:
            price = float(price_str.replace(',', '.'))
            max_price = 30_000_000
            return 0 < price <= max_price
        except ValueError:
            return False

    def is_valid_number(self, text):
        return text.strip().isdigit()

    def is_valid_driver_age(self, age_str):
        if not self.is_valid_number(age_str):
            return False, None
        age = int(age_str.strip())
        if 16 <= age <= 80:
            return True, age
        return False, None

    def is_valid_driver_exp(self, exp_str, max_exp):
        if not self.is_valid_number(exp_str):
            return False, None
        exp = int(exp_str.strip())
        if 0 <= exp <= max_exp:
            return True, exp
        return False, None

    def handle_vehicle_year(self, message):
        chat_id = message.chat.id
        year_str = message.text

        is_valid, is_in_range = self.is_valid_year(year_str)
        
        if is_valid:
            year = int(year_str)
            user_data[chat_id]["vehicle_year"] = year
            
            age, is_new, error_message = calc.define_age(manufacture_year=year)
            
            if error_message == "AGE_EXCEEDED":
                self.bot.send_message(
                    chat_id, 
                    strings.AGE_EXCEEDED_MESSAGE,
                    reply_markup=types.ReplyKeyboardRemove()
                )
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
                return
            
            if age is None:
                self.bot.send_message(chat_id, error_message or strings.INVALID_INPUT)
                self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)
                return
                
            user_data[chat_id]["vehicle_age_years"] = age
            user_data[chat_id]["is_new_vehicle"] = is_new
            
            self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def handle_vehicle_price(self, message):
        chat_id = message.chat.id
        price_str = message.text

        if self.is_valid_price(price_str):
            price = float(price_str.replace(',', '.'))
            user_data[chat_id]["vehicle_price_usd"] = price
            user_data[chat_id]["vehicle_price_full"] = price
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("GEELY", "ИНАЯ МАРКА")
            self.bot.send_message(chat_id, "Выберите марку автомобиля", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE)
        else:
            self.bot.send_message(chat_id, f"{strings.INVALID_INPUT} Страховая сумма должна быть от 1 до 30,000,000 USD.")
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)

    def handle_vehicle_make(self, message):
        chat_id = message.chat.id
        response = message.text.upper()

        if response == "GEELY":
            user_data[chat_id]["vehicle_make"] = "GEELY"
            user_data[chat_id]["is_geely"] = True
            user_data[chat_id]["is_in_list"] = True
            user_data[chat_id]["is_multidrive"] = True
            user_data[chat_id]["drivers_known"] = False
            user_data[chat_id]["num_drivers"] = 1
            user_data[chat_id]["drivers_data"] = [{"age": 0, "experience": 0}]
            
            self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP_GEELY, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)
            
        elif response == "ИНАЯ МАРКА":
            user_data[chat_id]["is_geely"] = False
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("BMW")
            for make in values.VEHICLE_MAKES_IN_LIST:
                if make not in ["GEELY", "BMW"]:
                    markup.add(make)
            markup.add("ДРУГОЕ")
            self.bot.send_message(chat_id, "Выберите автомобиль из списка", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_IN_LIST)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("GEELY", "ИНАЯ МАРКА")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_bmw_model(self, message):
        chat_id = message.chat.id
        response = message.text
        
        if response in values.BMW_M_MODELS:
            user_data[chat_id]["bmw_model"] = response
            user_data[chat_id]["is_in_list"] = False
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)
            
        elif response == "Другая модель":
            user_data[chat_id]["bmw_model"] = "Другая модель"
            user_data[chat_id]["is_in_list"] = True
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            for model in values.BMW_M_MODELS:
                markup.add(model)
            markup.add("Другая модель")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_in_list(self, message):
        chat_id = message.chat.id
        response = message.text.upper()

        valid_makes = [make for make in values.VEHICLE_MAKES_IN_LIST if make != "GEELY"]
        
        if response == "BMW":
            user_data[chat_id]["vehicle_make"] = "BMW"
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            for model in values.BMW_M_MODELS:
                markup.add(model)
            markup.add("Другая модель")
            self.bot.send_message(chat_id, "Выберите модель BMW:", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_BMW_MODEL)
            
        elif response in valid_makes or response == "ДРУГОЕ":
            user_data[chat_id]["vehicle_make"] = response
            user_data[chat_id]["is_in_list"] = response in valid_makes
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for make in valid_makes:
                markup.add(make)
            markup.add("ДРУГОЕ")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_multidrive(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            can_list_drivers = (response == strings.YES_BUTTON.lower())
            
            user_data[chat_id]["is_multidrive"] = not can_list_drivers
            user_data[chat_id]["drivers_known"] = can_list_drivers
            user_data[chat_id]["num_drivers"] = 1
            user_data[chat_id]["drivers_data"] = []
            
            self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_driver_age(self, message):
        chat_id = message.chat.id
        response = message.text

        is_valid, age = self.is_valid_driver_age(response)
        if is_valid:
            user_data[chat_id]["drivers_data"] = [{"age": age, "experience": 0}]
            self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)
        else:
            self.bot.send_message(chat_id, "Введите возраст водителя только цифрами (например: 25). Возраст должен быть от 16 до 80 лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)

    def handle_driver_exp(self, message):
        chat_id = message.chat.id
        response = message.text
        
        if user_data[chat_id].get("is_geely", False):
            max_exp = 70
        else:
            max_exp = user_data[chat_id]["drivers_data"][0]["age"] - 16

        is_valid, exp = self.is_valid_driver_exp(response, max_exp)
        if is_valid:
            user_data[chat_id]["drivers_data"][0]["experience"] = exp
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Республика Беларусь", "Республика Беларусь и за её пределами")
            self.bot.send_message(chat_id, strings.ASK_TERRITORY, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_TERRITORY)
        else:
            if user_data[chat_id].get("is_geely", False):
                self.bot.send_message(chat_id, f"Введите стаж вождения только цифрами (например: 5). Стаж должен быть от 0 до {max_exp} лет.")
            else:
                self.bot.send_message(chat_id, f"Введите стаж вождения только цифрами (например: 5). Стаж должен быть от 0 до {max_exp} лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def handle_territory(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in ["республика беларусь", "республика беларусь и за ее пределами"]:
            user_data[chat_id]["territory"] = "Республика Беларусь" if response == "республика беларусь" else "Республика Беларусь и за её пределами"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_CREDIT_LEASING_PLEDGE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_CREDIT_LEASING_PLEDGE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Республика Беларусь", "Республика Беларусь и за её пределами")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_credit_leasing_pledge(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["credit_leasing_pledge"] = (response == strings.YES_BUTTON.lower())
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_GREEN_PLATES, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_GREEN_PLATES)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_green_plates(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["green_plates"] = (response == strings.YES_BUTTON.lower())
            self.proceed_to_licensed_parts_or_calc(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def proceed_to_licensed_parts_or_calc(self, chat_id):
        if user_data[chat_id]["vehicle_age_years"] < 3:
            user_data[chat_id]["licensed_parts"] = False
            self.calculate_and_send_premium_from_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_LICENSED_PARTS, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_LICENSED_PARTS)

    def handle_is_licensed_parts(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["licensed_parts"] = (response == strings.YES_BUTTON.lower())
            self.calculate_and_send_premium_from_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def calculate_and_send_premium_from_state(self, chat_id):
        dummy_message = type('obj', (object,), {'chat': type('obj', (object,), {'id': chat_id})})()
        self.calculate_and_send_premium(dummy_message)

    def calculate_and_send_premium(self, message):
        chat_id = message.chat.id
        try:
            data = user_data.get(chat_id, {})
            response_message = "Предварительный расчет страховой премии:\n\n"
            has_results = False
            error_messages = []

            for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
                calculation_data = {
                    "program": program_name,
                    "vehicle_age_years": data.get("vehicle_age_years", 0),
                    "vehicle_price_usd": data.get("vehicle_price_usd", 0),
                    "vehicle_price_full": data.get("vehicle_price_full", 0),
                    "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
                    "drivers_known": data.get("drivers_known", False),
                    "num_drivers": data.get("num_drivers", 1),
                    "drivers_data": data.get("drivers_data", []),
                    "is_geely": data.get("is_geely", False),
                    "is_multidrive": data.get("is_multidrive", False),
                    "territory": data.get("territory", "Республика Беларусь"),
                    "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                    "licensed_parts": data.get("licensed_parts", False),
                    "is_in_list": data.get("is_in_list", False),
                    "green_plates": data.get("green_plates", False),
                    "quarterly_payment": False
                }

                final_premium, error_message = calc.calculate_final_premium(calculation_data)
                if final_premium is not None:
                    final_premium = round(final_premium)
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
            self.bot.send_message(chat_id, strings.CALCULATION_ERROR.format(str(e)), reply_markup=types.ReplyKeyboardRemove())
            self.ask_quarterly_payment(message)

    def handle_quarterly_payment(self, message):
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["quarterly_payment"] = (response == strings.YES_BUTTON.lower())
            if user_data[chat_id]["quarterly_payment"]:
                try:
                    data = user_data.get(chat_id, {})
                    response_message = "Предварительный расчет страховой премии при ежеквартальной оплате:\n\n"
                    has_results = False
                    error_messages = []

                    for program_name in kasko_program.AVAILABLE_PROGRAMS.keys():
                        calculation_data = {
                            "program": program_name,
                            "vehicle_age_years": data.get("vehicle_age_years", 0),
                            "vehicle_price_usd": data.get("vehicle_price_usd", 0),
                            "vehicle_price_full": data.get("vehicle_price_full", 0),
                            "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
                            "drivers_known": data.get("drivers_known", False),
                            "num_drivers": data.get("num_drivers", 1),
                            "drivers_data": data.get("drivers_data", []),
                            "is_geely": data.get("is_geely", False),
                            "is_multidrive": data.get("is_multidrive", False),
                            "territory": data.get("territory", "Республика Беларусь"),
                            "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                            "licensed_parts": data.get("licensed_parts", False),
                            "is_in_list": data.get("is_in_list", False),
                            "green_plates": data.get("green_plates", False),
                            "quarterly_payment": True
                        }

                        final_premium, error_message = calc.calculate_final_premium(calculation_data)
                        if final_premium is not None:
                            final_premium = round(final_premium)
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
                    self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                    self.bot.delete_state(chat_id)
                except Exception as e:
                    print(f"Error in handle_quarterly_payment: {str(e)}")
                    self.bot.send_message(chat_id, strings.CALCULATION_ERROR.format(str(e)), reply_markup=types.ReplyKeyboardRemove())
                    self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                    self.bot.delete_state(chat_id)
            else:
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def ask_quarterly_payment(self, message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_QUARTERLY_PAYMENT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_QUARTERLY_PAYMENT)

    def run(self):
        print("Bot started...")
        self.bot.infinity_polling()