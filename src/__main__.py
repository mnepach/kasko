from .kaskobot.telegram_bot import TelegramBot

def main():

    TOKEN = "8039071528:AAHwxMPFfUOaLgD13WYoVIhsJRqTGxF5d9w"
    bot = TelegramBot(TOKEN)
    bot.run()

if __name__ == "__main__":
    main()