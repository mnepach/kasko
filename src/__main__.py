from .kaskobot.telegram_bot import TelegramBot

def main():

    TOKEN = "8260339036:AAG7yFUiVXRLuEY0e9g2rHUh9DijjQEcKnc"
    bot = TelegramBot(TOKEN)
    bot.run()

if __name__ == "__main__":
    main()