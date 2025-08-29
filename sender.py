import os
from dotenv import load_dotenv
from main import price_currency, price_gold, price_crypto, date_time
import telebot

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = telebot.TeleBot(API_TOKEN)

def main():
    my_message = date_time()
    my_message += '\n<b>-------⬇️ نرخ ارز ⬇️--------</b>\n\n'
    my_message += price_currency()
    my_message += '\n<b>-------⬇️ قیمت ارزهای دیجیتال ⬇️--------</b>\n\n'
    my_message += price_crypto()
    my_message += '\n<b>-------⬇️ قیمت طلا ⬇️--------</b>\n\n'
    my_message += price_gold()
    bot.send_message(CHANNEL_ID, my_message, parse_mode='HTML')

if __name__ == '__main__':
    main()
