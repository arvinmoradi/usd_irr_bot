import os
import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import jdatetime

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
    keyboard.row(
        telebot.types.InlineKeyboardButton('کانال 1', url=f'https://t.me/{CHANNEL_LINK}'),
        telebot.types.InlineKeyboardButton('کانال 2', url=f'https://t.me/{CHANNEL_LINK_2}')
    )
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
        bot.send_message(
            call.message.chat.id,
            f'سلام به ربات استعلام قیمت ساخته شده توسط ArM خوش آمدید 👋🌹\nقیمت ها هر نیم ساعت یکبار به این کانال ارسال خواهند شد\nChannel: @{CHANNEL_LINK}',
            reply_markup=reply_keyboard()
        )
    else:
        bot.send_message(call.message.chat.id, '❌ هنوز عضو کانال‌ها نشده‌اید.')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        inline_keyboard(call.message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_member(message):
        bot.send_message(
            message.chat.id,
            f'سلام به ربات استعلام قیمت ساخته شده توسط ArM خوش آمدید 👋🌹\nقیمت ها هر نیم ساعت یکبار به این کانال ارسال خواهند شد\nChannel: @{CHANNEL_LINK}',
            reply_markup=reply_keyboard()
        )

@bot.message_handler(func=lambda msg: msg.text == 'ارتباط با پشتیبانی')
def support(message):
    bot.send_message(message.chat.id, f"برای ارتباط با پشتیبانی به آیدی زیر پیام دهید\nSupport ID : @{SUPPORT_ID}")

def date_time():
    weekdays_fa = {
        "Saturday": "شنبه",
        "Sunday": "یک‌شنبه",
        "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه",
        "Wednesday": "چهارشنبه",
        "Thursday": "پنج‌شنبه",
        "Friday": "جمعه",
    }
    now = jdatetime.datetime.now()
    weekdays_en = now.strftime('%A')
    date = now.strftime('%Y %m %d')
    text = f"<b>روز : {weekdays_fa[weekdays_en]}</b>\n<b>تاریخ : {date.replace(' ', '/')}</b>\n"
    return text

def price_currency():
    try:
        url = requests.get('https://www.tgju.org/currency')
        soup = BeautifulSoup(url.content, 'html.parser')
        attrs_list = ["price_dollar_rl", "price_eur", "price_gbp", "price_try", "price_iqd", "price_aed", "price_cny"]
        name_list = ['USD', 'EUR', 'GBP', 'TRY', 'IQD', 'AED', 'CNY']
        name_fa_list = ['دلار آمریکا', 'یورو', 'پوند انگلیس', 'لیر ترکیه', 'دینار عراق', 'درهم امارات', 'یوان چین']
        flag_list = ['🇺🇸', '🇪🇺', '🇬🇧', '🇹🇷', '🇮🇶', '🇦🇪', '🇨🇳']
        result_list = []
        text = ''
        for item in attrs_list:
            tr = soup.find('tr', attrs={"data-market-row": item})
            result = tr.find('td', class_='nf').text
            result = result.replace(',', '')
            result_list.append(result)
        for i in range(len(attrs_list)):
            text += f"<b>{flag_list[i]}-{name_fa_list[i]}({name_list[i]}): {(int(result_list[i]) // 10):,} تومان 💸</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')
        return '❌ خطا در دریافت قیمت ارز'
    
def price_crypto():
    try:
        url = 'https://apiv2.nobitex.ir/market/stats'
        headers = {
            "Authorization": f"Token {NOBITEX_TOKEN}",
            "content-type": "application/json"
        }
        data = {"dstCurrency": "rls"}
        text = ''
        crypto_dict = {
            'USDT': 'usdt-rls',
            'BTC': 'btc-rls',
            'ETH': 'eth-rls',
            'LTC': 'ltc-rls',
            'DOGE': 'doge-rls',
            'TRON': 'trx-rls',
            'TON': 'ton-rls'
        }
        farsi_names = {
            'USDT': 'تتر',
            'BTC': 'بیت کوین',
            'ETH': 'اتریوم',
            'LTC': 'لایت کوین',
            'DOGE': 'دوج کوین',
            'TRON': 'ترون',
            'TON': 'تون'
        }
        price = requests.get(url, headers=headers, data=data).json()
        for item in crypto_dict:
            items = int(price['stats'][crypto_dict[item]]['latest']) // 10
            text += f"<b>{farsi_names[item]}({item}): {items:,} تومان 💸</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')
        return '❌ خطا در دریافت قیمت کریپتو'
    
def price_gold():
    try:
        url = requests.get('https://www.tgju.org/gold-chart')
        soup = BeautifulSoup(url.content, 'html.parser')
        attrs_list = ['geram18', 'gold_740k', 'geram24', 'gold_mini_size']
        name_list = ['طلای 18 عیار-750', 'طلای 18 عیار-740', 'طلای 24 عیار', 'طلای دست دوم']
        emoji_list = ['🏅', '🏅', '🏅', '🏅']
        result_list = []
        text = ''
        for item in attrs_list:
            tr = soup.find('tr', attrs={'data-market-row': item})
            result = tr.find('td', class_='nf').text
            result = result.replace(',', '')
            result_list.append(result)
        for i in range(len(attrs_list)):
            text += f"<b>{name_list[i]}{emoji_list[i]} = {(int(result_list[i]) // 10):,} تومان 💸</b>\n\n"
        return text
    except Exception as e:
        print(f'Error connecting to the website\n{e}')
        return '❌ خطا در دریافت قیمت طلا'

# فقط ربات اجرا می‌شود
if __name__ == '__main__':
    bot.infinity_polling()