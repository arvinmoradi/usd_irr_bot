import os
import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
NOBITEX_TOKEN = os.getenv('NOBITEX_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_ID_2 = os.getenv('CHANNEL_ID_2')
CHANNEL_LINK = 'price_currency_and_crypto'
CHANNEL_LINK_2 = 'ArM_VPN_VIP'
SUPPORT_ID = 'ArvinMoradi'
bot = telebot.TeleBot(API_TOKEN)

def reply_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('ارتباط با پشتیبانی'))
    return markup

def inline_keyboard(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('کانال 1', url=f'https://t.me/{CHANNEL_LINK}'), telebot.types.InlineKeyboardButton('کانال 2', url=f'https://t.me/{CHANNEL_LINK_2}'))
    keyboard.row(telebot.types.InlineKeyboardButton('تایید عضویت✅', callback_data='check_member'))
    bot.send_message(message.chat.id, 'برای دریافت خدمات از ربات، باید در کانال های زیر عضو شوید', reply_markup=keyboard)

def is_member(message):
    def check(channel_id):
        user_info = bot.get_chat_member(channel_id, message.from_user.id)
        return user_info.status in ['administrator', 'creator', 'member']
    
    if check(CHANNEL_ID) and check(CHANNEL_ID_2):
        return True
    inline_keyboard(message)
    return False

@bot.callback_query_handler(func=lambda call: call.data == 'check_member')
def handle_callback(call):
    def check(channel_id):
        user_info = bot.get_chat_member(channel_id, call.from_user.id)
        return user_info.status in ['administrator', 'creator', 'member']
    
    if check(CHANNEL_ID) and check(CHANNEL_ID_2):
        bot.send_message(call.message.chat.id, '✅ عضویت شما تایید شد')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'سلام به ربات استعلام قیمت ساخته شده توسط ArM خوش آمدید 👋🌹\nقیمت ها هر نیم ساعت یکبار به این کانال ارسال خواهند شد\nChannel: @{CHANNEL_LINK}', 
                         reply_markup=reply_keyboard())
    else:
        bot.send_message(call.message.chat.id, '❌ هنوز عضو کانال‌ها نشده‌اید.')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        inline_keyboard(call.message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_member(message):
        bot.send_message(message.chat.id, f'سلام به ربات استعلام قیمت ساخته شده توسط ArM خوش آمدید 👋🌹\nقیمت ها هر نیم ساعت یکبار به این کانال ارسال خواهند شد\nChannel: @{CHANNEL_LINK}', 
                         reply_markup=reply_keyboard())
        
@bot.message_handler(func=lambda msg: msg.text == 'ارتباط با پشتیبانی')
def support(message):
    bot.send_message(message.chat.id, f"برای ارتباط با پشتیبانی به آیدی زیر پیام دهید\nSupport ID : @{SUPPORT_ID}")
    

def price_currency():
    try:
        url = requests.get('https://www.tgju.org/currency')
        soup = BeautifulSoup(url.content, 'html.parser')
        attrs_list = ["price_dollar_rl", "price_eur", "price_gbp", "price_try", "price_iqd", "price_aed"]
        name_list = ['USD', 'EUR', 'POUND', 'TRY', 'IQD', 'AED']
        flag_list = ['🇺🇸', '🇪🇺', '🇬🇧', '🇹🇷', '🇮🇶', '🇦🇪']
        result_list = []
        text = ''
        for item in attrs_list:
            tr = soup.find('tr', attrs={"data-market-row":item})
            result = tr.find('td', class_='nf').text
            result_list.append(result)
        for i in range(len(attrs_list)):
            text += f"<b>{name_list[i]}{flag_list[i]} = {result_list[i]} IRR</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')

def price_gold():
    try:
        url = requests.get('https://www.tgju.org/gold-chart')
        soup = BeautifulSoup(url.content, 'html.parser')
        attrs_list = ['geram18', 'gold_740k', 'geram24', 'gold_mini_size']
        name_list = ['18K gold-750', '18K gold-740', '24K gold', 'Pre-owned gold']
        emoji_list = ['🏅', '🏅', '🏅', '🏅']
        result_list = []
        text = ''
        for item in attrs_list:
            tr = soup.find('tr', attrs={'data-market-row':item})
            result = tr.find('td', class_='nf').text
            result_list.append(result)
        for i in range(len(attrs_list)):
            text += f"<b>{name_list[i]}{emoji_list[i]} = {result_list[i]} IRR</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')

def price_crypto():
    try:
        url = 'https://api.nobitex.ir/market/stats'
        headers = {
            "Authorization": f"Token {NOBITEX_TOKEN}",
            "content-type": "application/json"
        }
        data = {"dstCurrency":"rls"}
        text = ''
        crypto_dict = {
            'USDT' : 'usdt-rls',
            'BTC' : 'btc-rls',
            'ETH' : 'eth-rls',
            'LTC' : 'ltc-rls',
            'DOGE' : 'doge-rls',
            'TRON' : 'trx-rls',
            'TON' : 'ton-rls'
        }
        price = requests.post(url, headers=headers, json=data).json()
        for item in crypto_dict:
            items = '{:,}'.format(int(price['stats'][crypto_dict[item]]['latest']))
            text += f"<b>{item} = {items} IRR</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')
        
def main():
    my_message = '<b><i>-------⬇️ Currency ⬇️--------</i></b>\n\n'
    currency = price_currency()
    my_message += currency
    my_message += '\n<b><i>-------⬇️ Gold ⬇️--------</i></b>\n\n'
    gold = price_gold()
    my_message += gold
    my_message += '\n<b><i>-------⬇️ Crypto ⬇️--------</i></b>\n\n'
    crypto = price_crypto()
    my_message += crypto
    bot.send_message(CHANNEL_ID, my_message, parse_mode='HTML')

if __name__ == '__main__':
    main()
    
bot.infinity_polling()