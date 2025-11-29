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
user_has_started = {}

class BotState(StatesGroup):
    ASK_VEHICLE_YEAR = State()
    ASK_VEHICLE_PRICE = State()
    ASK_VEHICLE_MAKE = State()
    ASK_BMW_MODEL = State()
    ASK_IS_IN_LIST = State()
    ASK_IS_MULTIDRIVE = State()
    ASK_MULTIDRIVE_LESS_2_YEARS = State()
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
        self.bot.message_handler(content_types=['sticker','animation','photo','document','video','voice','location','contact'])(self.handle_invalid_content)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_YEAR)(self.handle_vehicle_year)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_PRICE)(self.handle_vehicle_price)
        self.bot.message_handler(state=BotState.ASK_VEHICLE_MAKE)(self.handle_vehicle_make)
        self.bot.message_handler(state=BotState.ASK_BMW_MODEL)(self.handle_bmw_model)
        self.bot.message_handler(state=BotState.ASK_IS_IN_LIST)(self.handle_is_in_list)
        self.bot.message_handler(state=BotState.ASK_IS_MULTIDRIVE)(self.handle_is_multidrive)
        self.bot.message_handler(state=BotState.ASK_MULTIDRIVE_LESS_2_YEARS)(self.handle_multidrive_less_2_years)
        self.bot.message_handler(state=BotState.ASK_DRIVER_AGE)(self.handle_driver_age)
        self.bot.message_handler(state=BotState.ASK_DRIVER_EXP)(self.handle_driver_exp)
        self.bot.message_handler(state=BotState.ASK_TERRITORY)(self.handle_territory)
        self.bot.message_handler(state=BotState.ASK_IS_CREDIT_LEASING_PLEDGE)(self.handle_is_credit_leasing_pledge)
        self.bot.message_handler(state=BotState.ASK_GREEN_PLATES)(self.handle_green_plates)
        self.bot.message_handler(state=BotState.ASK_IS_LICENSED_PARTS)(self.handle_is_licensed_parts)
        self.bot.message_handler(state=BotState.ASK_QUARTERLY_PAYMENT)(self.handle_quarterly_payment)
        self.bot.message_handler(func=lambda m: True)(self.catch_all)

    def catch_all(self, message):
        chat_id = message.chat.id
        if chat_id not in user_has_started or not user_has_started[chat_id]:
            user_has_started[chat_id] = True
            self.bot.send_message(chat_id, strings.INITIAL_WELCOME_MESSAGE, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            self.bot.send_message(chat_id, strings.THANK_YOU, parse_mode='Markdown')

    def send_welcome(self, message):
        chat_id = message.chat.id
        user_has_started[chat_id] = True
        user_data[chat_id] = {}
        self.bot.send_message(chat_id, strings.WELCOME_MESSAGE, parse_mode='Markdown', disable_web_page_preview=True)
        self.bot.send_message(chat_id, strings.ASK_VEHICLE_YEAR)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_YEAR)

    def send_help(self, message):
        self.bot.send_message(message.chat.id, strings.HELP_MESSAGE, parse_mode='Markdown', disable_web_page_preview=True)

    def handle_invalid_content(self, message):
        self.bot.send_message(message.chat.id, "Пожалуйста, используйте только текст и кнопки")

    def is_valid_year(self, text):
        try:
            year = int(text)
            current = datetime.now().year
            return current - 7 <= year <= current, year
        except:
            return False, None

    def is_valid_price(self, text):
        try:
            price = float(text.replace(',', '.'))
            return 0 < price <= 30_000_000, price
        except:
            return False, None

    def is_valid_age(self, text):
        try:
            age = int(text)
            return 16 <= age <= 80, age
        except:
            return False, None

    def handle_vehicle_year(self, message):
        chat_id = message.chat.id
        valid, year = self.is_valid_year(message.text)
        if not valid:
            self.bot.send_message(chat_id, strings.AGE_EXCEEDED_MESSAGE, parse_mode='Markdown')
            self.bot.send_message(chat_id, strings.THANK_YOU, parse_mode='Markdown')
            self.bot.delete_state(chat_id)
            return

        age, is_new, err = calc.define_age(year)
        if err == "AGE_EXCEEDED":
            self.bot.send_message(chat_id, strings.AGE_EXCEEDED_MESSAGE, parse_mode='Markdown')
            self.bot.send_message(chat_id, strings.THANK_YOU, parse_mode='Markdown')
            self.bot.delete_state(chat_id)
            return

        user_data[chat_id].update({
            "vehicle_year": year,
            "vehicle_age_years": age,
            "is_new_vehicle": is_new
        })

        self.bot.send_message(chat_id, strings.ASK_VEHICLE_PRICE, parse_mode='Markdown', disable_web_page_preview=True)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_PRICE)

    def handle_vehicle_price(self, message):
        chat_id = message.chat.id
        valid, price = self.is_valid_price(message.text)
        if not valid:
            self.bot.send_message(chat_id, "Введите корректную сумму цифрами (например: 25000)")
            return

        user_data[chat_id]["vehicle_price_usd"] = price
        user_data[chat_id]["vehicle_price_full"] = price

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("GEELY/BELGEE", "ИНАЯ МАРКА")
        self.bot.send_message(chat_id, "Выберите марку автомобиля:", reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_VEHICLE_MAKE)

    def handle_vehicle_make(self, message):
        chat_id = message.chat.id
        text = message.text.upper()

        if text == "GEELY/BELGEE":
            user_data[chat_id].update({
                "is_geely": True,
                "is_in_list": True,
                "is_multidrive": True,
                "drivers_known": False,
                "credit_leasing_pledge": False
            })
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(strings.DRIVER_EXP_LESS_1, strings.DRIVER_EXP_1_TO_2, strings.DRIVER_EXP_MORE_2)
            self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP_GEELY, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)
            return

        if text == "ИНАЯ МАРКА":
            user_data[chat_id]["is_geely"] = False
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add("BMW")
            for m in values.VEHICLE_MAKES_IN_LIST:
                if m not in ["GEELY/BELGEE", "BMW"]:
                    markup.add(m)
            markup.add("ДРУГОЕ")
            self.bot.send_message(chat_id, "Выберите марку из списка:", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_IN_LIST)
            return

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("GEELY/BELGEE", "ИНАЯ МАРКА")
        self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_is_in_list(self, message):
        chat_id = message.chat.id
        text = message.text.upper()

        if text == "BMW":
            user_data[chat_id]["vehicle_make"] = "BMW"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for model in values.BMW_M_MODELS:
                markup.add(model)
            markup.add("Другая модель")
            self.bot.send_message(chat_id, "Выберите модель BMW:", reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_BMW_MODEL)
            return

        user_data[chat_id]["is_in_list"] = text in values.VEHICLE_MAKES_IN_LIST
        user_data[chat_id]["vehicle_make"] = text if text != "ДРУГОЕ" else "Другое"

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, parse_mode='Markdown', reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)

    def handle_bmw_model(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["is_in_list"] = message.text not in values.BMW_M_MODELS
        user_data[chat_id]["bmw_model"] = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_IS_MULTIDRIVE, parse_mode='Markdown', reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_IS_MULTIDRIVE)

    def handle_is_multidrive(self, message):
        chat_id = message.chat.id
        ans = message.text.strip().lower()
        if ans == strings.YES_BUTTON.lower():
            user_data[chat_id]["is_multidrive"] = False
            user_data[chat_id]["drivers_known"] = True
            self.bot.send_message(chat_id, strings.ASK_DRIVER_AGE)
            self.bot.set_state(chat_id, BotState.ASK_DRIVER_AGE)
        elif ans == strings.NO_BUTTON.lower():
            user_data[chat_id]["is_multidrive"] = True
            user_data[chat_id]["drivers_known"] = False
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_MULTIDRIVE_LESS_2_YEARS, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_MULTIDRIVE_LESS_2_YEARS)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)

    def handle_multidrive_less_2_years(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["multidrive_has_less_2_years"] = message.text.lower() == strings.YES_BUTTON.lower()

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False, row_width=1)
        markup.add("Республика Беларусь")
        markup.add("Республика Беларусь и за её пределами")
        self.bot.send_message(chat_id, strings.ASK_TERRITORY, parse_mode='Markdown', reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_TERRITORY)

    def handle_driver_age(self, message):
        chat_id = message.chat.id
        valid, age = self.is_valid_age(message.text)
        if not valid:
            self.bot.send_message(chat_id, "Возраст должен быть от 16 до 80 лет")
            return
        user_data[chat_id]["driver_age"] = age

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(strings.DRIVER_EXP_LESS_1, strings.DRIVER_EXP_1_TO_2, strings.DRIVER_EXP_MORE_2)
        self.bot.send_message(chat_id, strings.ASK_DRIVER_EXP, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_DRIVER_EXP)

    def handle_driver_exp(self, message):
        chat_id = message.chat.id
        t = message.text.lower()
        if t == strings.DRIVER_EXP_LESS_1.lower():
            exp = 0
        elif t == strings.DRIVER_EXP_1_TO_2.lower():
            exp = 1
        elif t == strings.DRIVER_EXP_MORE_2.lower():
            exp = 2
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(strings.DRIVER_EXP_LESS_1, strings.DRIVER_EXP_1_TO_2, strings.DRIVER_EXP_MORE_2)
            self.bot.send_message(chat_id, strings.INVALID_INPUT, reply_markup=markup)
            return

        user_data[chat_id]["driver_exp"] = exp

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False, row_width=1)
        markup.add("Республика Беларусь")
        markup.add("Республика Беларусь и за её пределами")
        self.bot.send_message(chat_id, strings.ASK_TERRITORY, parse_mode='Markdown', reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_TERRITORY)

    def handle_territory(self, message):
        chat_id = message.chat.id
        text = message.text
        territory = "Республика Беларусь и за её пределами" if "за её" in text or "за ее" in text else "Республика Беларусь"
        user_data[chat_id]["territory"] = territory

        if user_data[chat_id].get("is_geely", False):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_GREEN_PLATES, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_GREEN_PLATES)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_CREDIT_LEASING_PLEDGE, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_CREDIT_LEASING_PLEDGE)

    def handle_is_credit_leasing_pledge(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["credit_leasing_pledge"] = message.text.lower() == strings.YES_BUTTON.lower()

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_GREEN_PLATES, reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_GREEN_PLATES)

    def handle_green_plates(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["green_plates"] = message.text.lower() == strings.YES_BUTTON.lower()

        if user_data[chat_id]["vehicle_age_years"] < 3:
            user_data[chat_id]["licensed_parts"] = False
            self.calculate_and_send_premium(message)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
            markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
            self.bot.send_message(chat_id, strings.ASK_IS_LICENSED_PARTS, reply_markup=markup)
            self.bot.set_state(chat_id, BotState.ASK_IS_LICENSED_PARTS)

    def handle_is_licensed_parts(self, message):
        chat_id = message.chat.id
        user_data[chat_id]["licensed_parts"] = message.text.lower() == strings.YES_BUTTON.lower()
        self.calculate_and_send_premium(message)

    def prepare_calculation_data(self, chat_id, quarterly_payment=False):
        data = user_data.get(chat_id, {})

        drivers_data = []
        if data.get("drivers_known"):
            drivers_data = [{"age": data.get("driver_age", 30), "experience": data.get("driver_exp", 2)}]
        elif data.get("is_multidrive"):
            exp = 0 if data.get("multidrive_has_less_2_years") else 2
            drivers_data = [{"age": 30, "experience": exp}]

        return {
            "program": None,
            "vehicle_age_years": data.get("vehicle_age_years", 0),
            "vehicle_price_usd": data.get("vehicle_price_usd", 20000),
            "vehicle_price_full": data.get("vehicle_price_full", 20000),
            "vehicle_type_group": values.VEHICLE_TYPE_PASSENGER_LIGHT_TRUCK,
            "drivers_known": data.get("drivers_known", False),
            "drivers_data": drivers_data,
            "is_geely": data.get("is_geely", False),
            "is_multidrive": data.get("is_multidrive", False),
            "territory": data.get("territory", "Республика Беларусь"),
            "credit_leasing_pledge": data.get("credit_leasing_pledge", False),
            "licensed_parts": data.get("licensed_parts", False),
            "is_in_list": data.get("is_in_list", True),
            "green_plates": data.get("green_plates", False),
            "quarterly_payment": quarterly_payment
        }

    def calculate_and_send_premium(self, message):
        chat_id = message.chat.id
        response = "Предварительная стоимость полиса при единовременной оплате:\n\n"
        has_results = False
        errors = []

        for program_name in kasko_program.AVAILABLE_PROGRAMS:
            calc_data = self.prepare_calculation_data(chat_id, quarterly_payment=False)
            calc_data["program"] = program_name
            premium, err = calc.calculate_final_premium(calc_data)
            if premium is not None:
                response += f"• {program_name}: *{premium:,} USD*\n".replace(",", " ")
                has_results = True
            else:
                errors.append(f"{program_name}: {err}")

        if has_results:
            response += f"\nДля точного расчета — @StrahovanieMinsk"
            if errors:
                response += "\n\nНе рассчитано:\n" + "\n".join(errors)
        else:
            response = "Не удалось рассчитать.\nОбратитесь к @StrahovanieMinsk"

        self.bot.send_message(chat_id, response, parse_mode='Markdown')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)
        markup.add(strings.YES_BUTTON, strings.NO_BUTTON)
        self.bot.send_message(chat_id, strings.ASK_QUARTERLY_PAYMENT, parse_mode='Markdown', reply_markup=markup)
        self.bot.set_state(chat_id, BotState.ASK_QUARTERLY_PAYMENT)

    def handle_quarterly_payment(self, message):
        chat_id = message.chat.id
        if message.text.lower() != strings.YES_BUTTON.lower():
            self.bot.send_message(chat_id, strings.THANK_YOU, parse_mode='Markdown')
            self.bot.delete_state(chat_id)
            return

        response = "Предварительная стоимость при оплате частями:\n\n"
        has_results = False

        for program_name in kasko_program.AVAILABLE_PROGRAMS:
            calc_data = self.prepare_calculation_data(chat_id, quarterly_payment=True)
            calc_data["program"] = program_name
            premium, _ = calc.calculate_final_premium(calc_data)
            if premium is not None:
                response += f"• {program_name}: *{premium:,} USD*\n".replace(",", " ")
                has_results = True

        response += "\nЦена выше на ~10%.\nТочный расчёт — @StrahovanieMinsk"

        self.bot.send_message(chat_id, response, parse_mode='Markdown')
        self.bot.send_message(chat_id, strings.THANK_YOU, parse_mode='Markdown')
        self.bot.delete_state(chat_id)

    def run(self):
        print("Bot started...")
        self.bot.infinity_polling()