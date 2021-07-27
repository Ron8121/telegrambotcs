import requests
import hmac
import hashlib
from datetime import datetime, timedelta
from config import MERCH_API, MERCH_ID, MERCH_BOT_URL
import time

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup,InputFile


async def keyboard(lang,url):
    markup = InlineKeyboardMarkup()
    if lang == "ru":
        markup.add(InlineKeyboardButton("Перейти на страничку оплаты", url=url))
        markup.add(InlineKeyboardButton("Проверить оплату",callback_data="check_pay"))
        text = """
        💎Оплата
        
        Нажмите на кнопку "Перейти на страничку оплаты"
        После оплаты подождите 2 минуты  и нажмите "Проверить оплату"
        """
    elif lang == "ua":
        markup.add(InlineKeyboardButton("Перейти на сторінку оплати",url=url))
        markup.add(InlineKeyboardButton("Провірити оплату",callback_data="check_pay"))
        text = """
        💎Оплата
        
        Нажміть на кнопку "Перейти на сторінку оплати"
        Після оплати почекайте 2 хвилини і нажміть "Провірити оплату"
        """
    elif lang == "en":
        markup.add(InlineKeyboardButton("Redirect to pay page",url=url))
        markup.add(InlineKeyboardButton("Check payments",callback_data="check_pay"))
        text = """
        💎Deposit
        
        Push button "Redirect to pay page"
        After pay wait 2 minuts then push "Check payments"
        """
    return markup,text





class Payments:
    def __init__(self,code):
        self.merchant_key = MERCH_API
        self.merchant_id = MERCH_ID
        self.url = MERCH_BOT_URL
        self.code = str(code) + str(int(time.time()))

    async def get_form_url(self,amount,user_id):
        amount = str(amount) + ".00"
        begin,_ = await self.get_time()
        head = {            
        "merchantAccount":self.merchant_id,
        "merchantDomainName": self.url,
        "merchantSignature": await self.generate_signature(self.merchant_key, f"{self.merchant_id};{self.url};{self.code};{begin};{amount};UAH;{self.code};1;{amount}"),
        "orderReference":str(self.code),
        "orderDate": begin,
        "amount":amount,
        "currency":"UAH",
        "productName":[str(self.code)],
        "productPrice":[amount],
        "productCount":[1]
        }
        response = requests.post("https://secure.wayforpay.com/pay?behavior=offline", json=head)
        return response.json()['url']

    async def check_success_payment(self):
        head ={
            "transactionType":"CHECK_STATUS",
            "merchantAccount": self.merchant_id,
            "orderReference": str(self.code),
            "merchantSignature": await self.generate_signature(self.merchant_key, f"{self.merchant_id};{str(self.code)}"),
            "apiVersion": 1
        }
        response = requests.post("https://api.wayforpay.com/api", json=head).json()
        if response['orderReference'] == str(self.code) and response['transactionStatus'] == 'Approved':
            return True, response['amount']
        return False, None
        



    async def generate_signature(self,merchant_key, data_str):
        return hmac.new(merchant_key.encode(), data_str.encode(), hashlib.md5).hexdigest()

    async def get_time(self):
        now = datetime.now()
        future = now + timedelta(minutes=5)
        begin = int(datetime.timestamp(now))
        end = int(datetime.timestamp(future))
        return begin,end
