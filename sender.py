import os
from dotenv import load_dotenv
from bot import price_currency, price_gold, price_crypto
import telebot

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = telebot.TeleBot(API_TOKEN)

def main():
    my_message = '<b><i>-------⬇️ Currency ⬇️--------</i></b>\n\n'
    my_message += price_currency()
    my_message += '\n<b><i>-------⬇️ Gold ⬇️--------</i></b>\n\n'
    my_message += price_gold()
    my_message += '\n<b><i>-------⬇️ Crypto ⬇️--------</i></b>\n\n'
    my_message += price_crypto()
    bot.send_message(CHANNEL_ID, my_message, parse_mode='HTML')

if __name__ == '__main__':
    main()
