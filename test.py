import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
NOBITEX_TOKEN = os.getenv('NOBITEX_TOKEN')


url = 'https://apiv2.nobitex.ir/market/stats'
headers = {
    'content-type': 'application/json'
}
data = {'dstCurrency': 'rls'} # برای معادل سازی ریالی ارزهای موردنظر

price = requests.get(url, headers=headers, data=data).json()
btc = int(price['stats']['btc-rls']['latest']) // 10
btc = f"{btc:,} IRT"

print(btc)