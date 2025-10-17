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
    ASK_IS_NEW_VEHICLE = State()
    ASK_VEHICLE_PRICE = State()
    ASK_VEHICLE_MAKE = State()
    ASK_IS_IN_LIST = State()
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
        """Register all message handlers for the bot."""
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['help'])(self.send_help)
        self.bot.message_handler(content_types=['sticker', 'animation', 'photo'])(self.handle_invalid_content)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_IS_NEW_VEHICLE)(self.handle_is_new_vehicle)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
        self.bot.message_handler(state=BotState.ASK_IS_IN_LIST)(self.handle_is_in_list)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_TERRITORY)(self.handle_territory)
        self.bot.message_handler(state=BotState.ASK_IS_CREDIT_LEASING_PLEDGE)(self.handle_is_credit_leasing_pledge)
        self.bot.message_handler(state=BotState.ASK_IS_LICENSED_PARTS)(self.handle_is_licensed_parts)
        self.bot.message_handler(state=BotState.ASK_QUARTERLY_PAYMENT)(self.handle_quarterly_payment)
        self.bot.message_handler(content_types=['text'])(self.handle_unexpected_text)

    def send_welcome(self, message):
        """Handle /start command and initialize user data."""
        chat_id = message.chat.id
        user_data[chat_id] = {}
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def send_help(self, message):
        """Handle /help command."""
        chat_id = message.chat.id
        self.bot.send_message(chat_id, strings.HELP_MESSAGE)

    def handle_invalid_content(self, message):
        """Handle invalid content types like stickers, GIFs, or photos."""
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Ошибка: отправка стикеров, GIF или фото не поддерживается. Пожалуйста, используйте текстовый ввод.")

    def handle_unexpected_text(self, message):
        """Handle unexpected text messages after calculation."""
        chat_id = message.chat.id
        if not self.bot.get_state(chat_id):
            self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())

    def is_valid_year(self, year_str):
        """Validate vehicle year input."""
        try:
            year = int(year_str)
            current_year = datetime.now().year
            max_vehicle_age = 7
            min_allowed_year = current_year - max_vehicle_age
            return min_allowed_year <= year <= current_year
        except ValueError:
            return False

    def is_valid_price(self, price_str):
        """Validate vehicle price input."""
        try:
            price = float(price_str.replace(',', '.'))
            max_price = 30_000_000
            return 0 < price <= max_price
        except ValueError:
            return False

    def extract_number(self, text):
        """Extract number from text, ignoring words like 'лет'."""
        try:
            number = re.match(r'^\d+', text.strip())
            if number:
                return int(number.group(0))
            return None
        except ValueError:
            return None

    def is_valid_driver_age(self, age_str):
        """Validate driver age input, allowing 'лет'."""
        age = self.extract_number(age_str)
        if age is not None and 16 <= age <= 80:
            return True, age
        return False, None

    def is_valid_driver_exp(self, exp_str, max_exp):
        """Validate driver experience input, allowing 'лет' or 'меньше года'."""
        if exp_str.lower().replace("ё", "е") == "меньше года":
            return True, 0
        exp = self.extract_number(exp_str)
        if exp is not None and 0 <= exp <= max_exp:
            return True, exp
        return False, None

    def handle_vehicle_year(self, message):
        """Handle vehicle year input."""
        chat_id = message.chat.id
        year_str = message.text

        if self.is_valid_year(year_str):
            user_data[chat_id]["vehicle_year"] = int(year_str)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.NEW_VEHICLE_BUTTON, strings.USED_VEHICLE_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_NEW_VEHICLE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_NEW_VEHICLE)
        else:
            self.bot.send_message(chat_id, strings.INVALID_INPUT)
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def handle_is_new_vehicle(self, message):
        """Handle new/used vehicle input."""
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.NEW_VEHICLE_BUTTON.lower(), strings.USED_VEHICLE_BUTTON.lower()]:
            user_data[chat_id]["is_new_vehicle"] = (response == strings.NEW_VEHICLE_BUTTON.lower())
            age, error_message = calc.define_age(
                manufacture_year=user_data[chat_id]["vehicle_year"],
                is_new_vehicle=user_data[chat_id]["is_new_vehicle"]
            )
            if age is None:
                self.bot.send_message(chat_id, error_message or strings.INVALID_INPUT)
                self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)
                return
            user_data[chat_id]["vehicle_age_years"] = age
            self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.NEW_VEHICLE_BUTTON, strings.USED_VEHICLE_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_vehicle_price(self, message):
        """Handle vehicle price input."""
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
        """Handle vehicle make input."""
        chat_id = message.chat.id
        response = message.text.upper()

        if response in values.MAKE_COEFFICIENTS:
            user_data[chat_id]["vehicle_make"] = response
            user_data[chat_id]["is_geely"] = response == "GEELY"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for make in values.VEHICLE_MAKES_IN_LIST:
                markup.add(make)
            markup.add("ДРУГОЕ")
            self.bot.send_message(chat_id, "Выберите автомобиль из списка", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_IN_LIST)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("GEELY", "ИНАЯ МАРКА")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_in_list(self, message):
        """Handle whether vehicle is in approved list."""
        chat_id = message.chat.id
        response = message.text.upper()

        if response in values.VEHICLE_MAKES_IN_LIST or response == "ДРУГОЕ":
            user_data[chat_id]["is_in_list"] = response in values.VEHICLE_MAKES_IN_LIST
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for make in values.VEHICLE_MAKES_IN_LIST:
                markup.add(make)
            markup.add("ДРУГОЕ")
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_multidrive(self, message):
        """Handle multidrive option input."""
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["is_multidrive"] = (response == strings.YES_BUTTON.lower())
            user_data[chat_id]["drivers_known"] = not user_data[chat_id]["is_multidrive"]
            user_data[chat_id]["num_drivers"] = 1
            user_data[chat_id]["drivers_data"] = []
            if user_data[chat_id]["is_multidrive"]:
                user_data[chat_id]["multidrive_2_plus_years_exp"] = True
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add("Республика Беларусь", "Республика Беларусь и за её пределами")
                self.bot.send_message(chat_id, strings.ASK_TERRITORY, reply_markup=markup)
                self.bot.set_state(chat_id, BotState.ASK_TERRITORY)
            else:
                self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE, reply_markup=types.ReplyKeyboardRemove())
                self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_driver_age(self, message):
        """Handle driver age input."""
        chat_id = message.chat.id
        response = message.text

        is_valid, age = self.is_valid_driver_age(response)
        if is_valid:
            user_data[chat_id]["drivers_data"] = [{"age": age, "experience": 0}]
            self.bot.send_message(chat_id, f"{strings.ASK_DRIVER_EXP} (Если стаж меньше года, введите '0' или 'меньше года')", reply_markup=types.ReplyKeyboardRemove())
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)
        else:
            self.bot.send_message(chat_id, "Возраст водителя должен быть от 16 до 80 лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)

    def handle_driver_exp(self, message):
        """Handle driver experience input."""
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")
        max_exp = user_data[chat_id]["drivers_data"][0]["age"] - 16

        is_valid, exp = self.is_valid_driver_exp(response, max_exp)
        if is_valid:
            user_data[chat_id]["drivers_data"][0]["experience"] = exp
            user_data[chat_id]["multidrive_2_plus_years_exp"] = exp >= 2
            user_data[chat_id]["geely_low_exp_coeff"] = values.COEFF_GEELY_LOW_EXP if user_data[chat_id]["is_geely"] and exp < 2 else 1.0
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Республика Беларусь", "Республика Беларусь и за её пределами")
            self.bot.send_message(chat_id, strings.ASK_TERRITORY, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_TERRITORY)
        else:
            self.bot.send_message(chat_id, f"Стаж вождения должен быть от меньше года (0) до {max_exp} лет.")
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def handle_territory(self, message):
        """Handle territory input."""
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
        """Handle credit/lease/pledge input."""
        chat_id = message.chat.id
        response = message.text.lower().replace("ё", "е")

        if response in [strings.YES_BUTTON.lower(), strings.NO_BUTTON.lower()]:
            user_data[chat_id]["credit_leasing_pledge"] = (response == strings.YES_BUTTON.lower())
            self.proceed_to_licensed_parts_or_calc(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def proceed_to_licensed_parts_or_calc(self, chat_id):
        """Proceed to licensed parts question or calculation based on vehicle age."""
        if user_data[chat_id]["vehicle_age_years"] < 3:
            user_data[chat_id]["licensed_parts"] = False
            self.calculate_and_send_premium_from_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_LICENSED_PARTS, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_LICENSED_PARTS)

    def handle_is_licensed_parts(self, message):
        """Handle licensed parts input."""
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
        """Helper method to trigger premium calculation."""
        dummy_message = type('obj', (object,), {'chat': type('obj', (object,), {'id': chat_id})})()
        self.calculate_and_send_premium(dummy_message)

    def calculate_and_send_premium(self, message):
        """Calculate and send the annual premium."""
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
                    "territory": data.get("territory", "Республика Беларусь"),
                    "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                    "licensed_parts": data.get("licensed_parts", False),
                    "multidrive_2_plus_years_exp": data.get("multidrive_2_plus_years_exp", False),
                    "is_in_list": data.get("is_in_list", False),
                    "quarterly_payment": False,
                    "geely_low_exp_coeff": data.get("geely_low_exp_coeff", 1.0)
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
        """Handle quarterly payment option and calculate quarterly premium."""
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
                            "territory": data.get("territory", "Республика Беларусь"),
                            "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
                            "licensed_parts": data.get("licensed_parts", False),
                            "multidrive_2_plus_years_exp": data.get("multidrive_2_plus_years_exp", False),
                            "is_in_list": data.get("is_in_list", False),
                            "quarterly_payment": True,
                            "geely_low_exp_coeff": data.get("geely_low_exp_coeff", 1.0)
                        }

                        final_premium, error_message = calc.calculate_final_premium(calculation_data)
                        if final_premium is not None:
                            quarterly_premium = calc.calculate_quarterly_premium(final_premium)
                            quarterly_premium = round(quarterly_premium)
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
            else:
                self.bot.send_message(chat_id, strings.THANK_YOU, reply_markup=types.ReplyKeyboardRemove())
                self.bot.delete_state(chat_id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def ask_quarterly_payment(self, message):
        """Ask if user wants quarterly payment calculation."""
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_QUARTERLY_PAYMENT, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_QUARTERLY_PAYMENT)

    def run(self):
        """Start the bot."""
        print("Bot started...")
        self.bot.infinity_polling()