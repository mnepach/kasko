# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import date

from .vehicle import Vehicle        
from .driver import Driver          
from .insurance import Insurance    
from ..res import values as val

class TelegramBot:
    (VEHICLE_YEAR, VEHICLE_PRICE, TERRITORY, IS_GEELY, IS_BMW,
     DRIVER_AGE, DRIVER_EXP, DRIVER_COUNT) = range(8)

    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self._setup_handlers()
        self.user_data = {} 

    def _setup_handlers(self):
        """Настройка обработчиков."""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start), MessageHandler(filters.Regex("^Старт$"), self.start)],
            states={
                self.VEHICLE_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.vehicle_year)],
                self.VEHICLE_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.vehicle_price)],
                self.TERRITORY: [MessageHandler(filters.Regex("^(Да|Нет)$"), self.territory)],
                self.IS_GEELY: [MessageHandler(filters.Regex("^(Да|Нет)$"), self.is_geely)],
                self.IS_BMW: [MessageHandler(filters.Regex("^(Да|Нет)$"), self.is_bmw)],
                self.DRIVER_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.driver_age)],
                self.DRIVER_EXP: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.driver_exp)],
                self.DRIVER_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.driver_count)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.app.add_handler(conv_handler)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.fallback_message))

    async def fallback_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправляет сообщение, если пользователь вводит что-то вне контекста ConversationHandler."""
        reply_keyboard = [["Старт"]]
        await update.message.reply_text(
            "Привет! 🚗 Я бот для расчета КАСКО. Нажми кнопку 'Старт' 👇, чтобы начать.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start или нажатия кнопки 'Старт'. Начало опроса."""
        user_id = update.effective_user.id
        self.user_data[user_id] = {} 
        await update.message.reply_text(
            "Привет! 🚗 Я бот для расчета КАСКО. Давайте начнем.\n"
            "Введите год выпуска автомобиля (например, 2020):",
            reply_markup=ReplyKeyboardRemove()
        )
        return self.VEHICLE_YEAR

    async def vehicle_year(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка года выпуска автомобиля."""
        user_id = update.effective_user.id
        year_str = update.message.text
        try:
            year = int(year_str)
            if 1900 <= year <= date.today().year + 1: 
                self.user_data[user_id]["vehicle_year"] = year
                await update.message.reply_text("Введите стоимость автомобиля (например, 15000.00):")
                return self.VEHICLE_PRICE
            else:
                await update.message.reply_text(
                    f"Пожалуйста, введите корректный год (от 1900 до {date.today().year + 1}):"
                )
                return self.VEHICLE_YEAR
        except ValueError:
            await update.message.reply_text("Некорректный формат года. Пожалуйста, введите число (например, 2020):")
            return self.VEHICLE_YEAR

    async def vehicle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка стоимости автомобиля."""
        user_id = update.effective_user.id
        price_str = update.message.text
        try:
            price = float(price_str)
            if price > 0:
                self.user_data[user_id]["vehicle_price"] = price
                reply_keyboard = [["Да", "Нет"]]
                await update.message.reply_text(
                    "Автомобиль используется только в Беларуси?",
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                )
                return self.TERRITORY
            else:
                await update.message.reply_text("Стоимость должна быть положительным числом. Пожалуйста, введите корректную стоимость:")
                return self.VEHICLE_PRICE
        except ValueError:
            await update.message.reply_text("Некорректный формат стоимости. Пожалуйста, введите число (например, 15000.00):")
            return self.VEHICLE_PRICE

    async def territory(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка вопроса о территории."""
        user_id = update.effective_user.id
        self.user_data[user_id]["territory"] = update.message.text == "Да"
        reply_keyboard = [["Да", "Нет"]]
        await update.message.reply_text(
            "Автомобиль марки GEELY?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.IS_GEELY

    async def is_geely(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка вопроса о марке GEELY."""
        user_id = update.effective_user.id
        self.user_data[user_id]["is_geely"] = update.message.text == "Да"
        reply_keyboard = [["Да", "Нет"]]
        await update.message.reply_text(
            "Автомобиль марки BMW?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.IS_BMW

    async def is_bmw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка вопроса о марке BMW."""
        user_id = update.effective_user.id
        self.user_data[user_id]["is_bmw"] = update.message.text == "Да"
        await update.message.reply_text(
            "Введите возраст водителя (например, 30):",
            reply_markup=ReplyKeyboardRemove()
        )
        return self.DRIVER_AGE

    async def driver_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка возраста водителя."""
        user_id = update.effective_user.id
        age_str = update.message.text
        try:
            age = int(age_str)
            if 18 <= age <= 100: # диапазон возраста
                self.user_data[user_id]["driver_age"] = age
                await update.message.reply_text("Введите стаж вождения в годах (например, 5):")
                return self.DRIVER_EXP
            else:
                await update.message.reply_text("Пожалуйста, введите корректный возраст (от 18 лет):")
                return self.DRIVER_AGE
        except ValueError:
            await update.message.reply_text("Некорректный формат возраста. Пожалуйста, введите число (например, 30):")
            return self.DRIVER_AGE

    async def driver_exp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка стажа вождения."""
        user_id = update.effective_user.id
        exp_str = update.message.text
        try:
            exp = int(exp_str)
            if 0 <= exp <= 80: 
                self.user_data[user_id]["driver_exp"] = exp
                await update.message.reply_text("Сколько водителей будет указано в полисе? (Введите 1, если один):")
                return self.DRIVER_COUNT
            else:
                await update.message.reply_text("Пожалуйста, введите корректный стаж (от 0 до 80):")
                return self.DRIVER_EXP
        except ValueError:
            await update.message.reply_text("Некорректный формат стажа. Пожалуйста, введите число (например, 5):")
            return self.DRIVER_EXP

    async def driver_count(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка количества водителей и запуск расчета."""
        user_id = update.effective_user.id
        count_str = update.message.text
        try:
            count = int(count_str)
            if count > 0:
                self.user_data[user_id]["driver_count"] = count

                user_data = self.user_data[user_id]

                vehicle = Vehicle() 
                vehicle.set_vehicle_production_year(user_data["vehicle_year"])
                vehicle.set_vehicle_price(user_data["vehicle_price"])
                vehicle.set_is_geely(user_data["is_geely"])
                vehicle.set_is_bmw(user_data["is_bmw"])

                drivers = []

                for _ in range(count):
                    driver = Driver() 
                    driver.set_driver_age(user_data["driver_age"])
                    driver.set_driver_expirience(user_data["driver_exp"])
                    driver.define_driver_rate() 
                    drivers.append(driver)

                curInsurance = Insurance() 
                curInsurance.set_vehicle_info(vehicle)
                curInsurance.set_drivers_info(drivers) 
                curInsurance.set_rb_only(user_data["territory"])

                curInsurance.set_rates_from_programs()
                curInsurance.calc_summary_values()

                result_message = "<b>Результаты расчета КАСКО:</b>\n\n"
                for program_name, total_price in curInsurance.totals_for_programs.items():
                    result_message += f"<b>Программа {program_name}:</b> {total_price:.2f} BYN\n"

                result_message += "\nСпасибо за использование бота! Нажмите 'Старт', чтобы начать заново."

                await update.message.reply_html(
                    result_message,
                    reply_markup=ReplyKeyboardMarkup([["Старт"]], one_time_keyboard=True)
                )
                self.user_data.pop(user_id, None) 
                return ConversationHandler.END
            else:
                await update.message.reply_text("Пожалуйста, введите корректное количество водителей (например, 1):")
                return self.DRIVER_COUNT
        except ValueError:
            await update.message.reply_text("Некорректный формат количества водителей. Пожалуйста, введите число (например, 1):")
            return self.DRIVER_COUNT

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена опроса."""
        user_id = update.effective_user.id
        self.user_data.pop(user_id, None)  
        await update.message.reply_text(
            "Опрос отменен. Нажмите 'Старт', чтобы начать заново.",
            reply_markup=ReplyKeyboardMarkup([["Старт"]], one_time_keyboard=True)
        )
        return ConversationHandler.END

    def run(self):
        """Запуск бота."""
        self.app.run_polling(drop_pending_updates=True)