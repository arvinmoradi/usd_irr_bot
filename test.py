import os
import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import jdatetime

load_dotenv()
API_TOKEN_TEST = os.getenv('API_TOKEN_TEST')
CHANNEL_ID_TEST = os.getenv('CHANNEL_ID_TEST')
NOBITEX_TOKEN = os.getenv('NOBITEX_TOKEN')

bot = telebot.TeleBot(API_TOKEN_TEST)

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
     
my_message = date_time()
my_message += '\n<b>-------⬇️ نرخ ارز ⬇️--------</b>\n\n'
my_message += price_currency()
my_message += '\n<b>-------⬇️ قیمت ارزهای دیجیتال ⬇️--------</b>\n\n'
my_message += price_crypto()
my_message += '\n<b>-------⬇️ قیمت طلا ⬇️--------</b>\n\n'
my_message += price_gold()

bot.send_message(CHANNEL_ID_TEST, my_message, parse_mode='HTML')

bot.infinity_polling()