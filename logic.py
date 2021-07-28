from main import dp, bot
import db
from aiogram import types
from aiogram.dispatcher import FSMContext 
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup,InputFile
from config import RULES, BOT_NAME, SUPPORT_LINK
import re
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import time
from payments import Payments
import payments
import threading

from aiogram.utils.deep_linking import decode_payload
from aiogram.types import Message


async def get_photo():
    n = open("photo.jpg",'rb')
    return n




# ==================== keyboards and languages ==================================


async def main_menu_ru():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)([[
        KeyboardButton("🖥 Личный кабинет"),
        KeyboardButton("🎯 Игры")],[
        KeyboardButton("📊 Статистика"),
        KeyboardButton("🛡 Тех.Поддержка")]]
        )
    inline = InlineKeyboardMarkup(resize_keyboard=True)().row(
        InlineKeyboardButton("💸 Пополнить",callback_data="deposit"),
        InlineKeyboardButton("⌛️ Вывести",callback_data="withdraw"),
        InlineKeyboardButton("🌐 Сменить язык", callback_data="cng_lang")
    )
    return markup,inline

async def main_menu_ua():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)([[
        KeyboardButton("🖥 Особистий кабінет"),
        KeyboardButton("🎯 Ігри")],[
        KeyboardButton("📊 Статистика"),
        KeyboardButton("🛡 Тех.Підтримка")]]
        )
    inline = InlineKeyboardMarkup(resize_keyboard=True)().row(
        InlineKeyboardButton("💸 Повнити",callback_data="deposit"),
        InlineKeyboardButton("⌛️ Вивести",callback_data="withdraw"),
        InlineKeyboardButton("🌐 Змінити мову", callback_data="cng_lang")
        )
    return markup,inline

async def main_menu_en():
    markup = ReplyKeyboardMarkup([[
        KeyboardButton("🖥 Personal cabinet"),
        KeyboardButton("🎯 Games")],[
        KeyboardButton("📊 Statistics"),
        KeyboardButton("🛡 Support")]]
        )
    inline = InlineKeyboardMarkup().row(
        InlineKeyboardButton("💸 Deposit",callback_data="deposit"),
        InlineKeyboardButton("⌛️ Withdraw",callback_data="withdraw"),
        InlineKeyboardButton("🌐 Change Lang", callback_data="cng_lang")
        )
    return markup,inline

async def cabinet(user_id):
    user = await db.get_user_data(user_id)
    rand = random.randint(508,517)
    if user[1] == 'ru':
        text = """🙋🏻‍♀️ Личный кабинет

💰Ваш баланс : {} UAH
🧑🏼‍💻Ваши рефералы : {}
💎 Ваша реферальная ссылка : http://t.me/{}?start={}

🧩 Число человек онлайн : {}
            """.format(user[2],user[3],BOT_NAME[1:],user[0],rand)
        key1,key2 = await main_menu_ru()
        return text, key1, key2

    elif user[1] == 'ua':
        text = """🙋🏻‍♀️ Особистий кабінет

💰Ваш баланс : {} UAH
🧑🏼‍💻Ваші реферали : {}
💎 Ваша реферальна силка : http://t.me/{}?start={}

🧩 Число людей онлайн : {}
            """.format(user[2],user[3],BOT_NAME[1:],user[0],rand)
        key1,key2 = await main_menu_ua()
        return text, key1, key2

    elif user[1] == 'en':
        text = """🙋🏻‍♀️ Personal cabinet

💰Your balance : {} UAH
🧑🏼‍💻Your referals : {}
💎Your referals link : http://t.me/{}?start={}

🧩 Players online : {}
            """.format(user[2],user[3],BOT_NAME[1:],user[0],rand)
        key1,key2 = await main_menu_en()
        return text, key1, key2

async def statistic_lang(lang):
    cnt_user = "15 048"
    max_balance = "198 357"
    if lang == 'ru':
        return """
Статистика {}

🧩 Всего игроков - {}

🎮 Максимальный выйгрыш- {} UAH

        """.format(BOT_NAME,cnt_user,max_balance)

    elif lang == 'ua':
        return """
Статистика {}

🧩 Всього гравців - {}

🎮 Максимальний виграш- {} UAH

        """.format(BOT_NAME,cnt_user,max_balance)

    elif lang == 'en':
        return """
Statistics {}

🧩 Players - {}

🎮 Max win- {} UAH

        """.format(BOT_NAME,cnt_user,max_balance)

#==================================================================================================
#     
 
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    exist = await db.user_exist(user_id)
    img:bytes = await get_photo()
    img.seek(0)
    PHOTO_COVER = InputFile(img)
    if message.get_args():
        args = int(message.get_args())
        if args != user_id:
            await db.change_referalse(args)
        


    if exist[0]:
        text,markup,_ = await cabinet(user_id)
        await bot.send_photo(user_id,PHOTO_COVER,text,reply_markup=markup)
    else:
        
        agree = InlineKeyboardButton("Соглашаюсь",callback_data="agreed")
        key1 =  InlineKeyboardMarkup()
        key1.add(agree)
        await bot.send_message(user_id,RULES,reply_markup=key1)


                                      
# ============================= registration =======================================================

@dp.callback_query_handler(lambda c: c.data == "agreed")
async def callback_registration(callback_query: types.CallbackQuery):

    await db.create_user(callback_query.from_user.id)

    lang_markup = InlineKeyboardMarkup()
    lang_markup.add(InlineKeyboardButton("UA",callback_data='lang:ua'))
    lang_markup.add(InlineKeyboardButton("RUS",callback_data='lang:ru'))
    lang_markup.add(InlineKeyboardButton("ENG",callback_data='lang:en'))  
    await bot.send_message(callback_query.from_user.id,'Выберите язык',reply_markup=lang_markup)

@dp.callback_query_handler(lambda c: c.data == "cng_lang")
async def callback_change_lang(callback_query: types.CallbackQuery):
    lang_markup = InlineKeyboardMarkup()
    lang_markup.add(InlineKeyboardButton("UA",callback_data='lang:ua'))
    lang_markup.add(InlineKeyboardButton("RUS",callback_data='lang:ru'))
    lang_markup.add(InlineKeyboardButton("ENG",callback_data='lang:en'))  
    await bot.send_message(callback_query.from_user.id,'Выберите язык',reply_markup=lang_markup)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lang:"))
async def callback_changelang(callback_query: types.CallbackQuery):
    img:bytes = await get_photo()
    img.seek(0)
    PHOTO_COVER = InputFile(img)
    await db.change_lang(callback_query.from_user.id,callback_query.data.split(":")[1])
    text,markup,inline = await cabinet(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,"Changed",reply_markup=markup)
    await bot.send_photo(callback_query.from_user.id,PHOTO_COVER,text,reply_markup=inline)
    
#=====================================================================================================

#================================== callbacks message ================================================
@dp.message_handler(lambda c: c.text == "Back" or c.text == "Назад")
async def callback_back_main_menu(message: types.Message):
    _,markup,_ = await cabinet(message.from_user.id)
    await bot.send_message(message.from_user.id,"🔙 🔙",reply_markup=markup)

@dp.message_handler(lambda c: c.text.startswith("🖥"))
async def callback_full_main_menu(message: types.Message):
    img:bytes = await get_photo()
    img.seek(0)
    PHOTO_COVER = InputFile(img)

    text,_,inline = await cabinet(message.from_user.id)
    await bot.send_photo(message.from_user.id,PHOTO_COVER,text,reply_markup=inline)

@dp.message_handler(lambda c: c.text.startswith("🛡"))
async def callback_support(message: types.Message):
    lang = await db.get_lang(message.from_user.id)
    if lang == 'ru':
        await bot.send_message(message.from_user.id,"Техническая поддержка: {}".format(SUPPORT_LINK))
    elif lang == 'ua':
        await bot.send_message(message.from_user.id,"Технічна підтримка: {}".format(SUPPORT_LINK))
    elif lang == 'en':
        await bot.send_message(message.from_user.id,"Support: {}".format(SUPPORT_LINK))
    
@dp.message_handler(lambda c: c.text.startswith("📊"))
async def callback_statistic(message: types.Message):
    lang = await db.get_lang(message.from_user.id)
    text = await statistic_lang(lang)
    await bot.send_message(message.from_user.id,text)

@dp.message_handler(lambda c: c.text.startswith("🎯"))
async def callback_games(message: types.Message):
    lang = await db.get_lang(message.from_user.id)
    x = lambda : "Back" if lang == 'en' else 'Назад'
    markup = ReplyKeyboardMarkup([[
            KeyboardButton("🎰 CASINO 🎰"),
            #KeyboardButton("📈 CRASH 📈")
            ],[
                #KeyboardButton("🗄 SAFE 🗄"),
                KeyboardButton("🎲 DICE 🎲")
            ],[
                KeyboardButton(x())
            ]])
    if lang == 'ru':
        await bot.send_message(message.from_user.id,'Выберите интересующую Вас игру', reply_markup=markup)
    elif lang == 'ua':
        await bot.send_message(message.from_user.id,'Виберіть цікаву для Вас ігру', reply_markup=markup)
    elif lang == 'en':
        await bot.send_message(message.from_user.id,'Choose your game', reply_markup=markup)
#===========================================================================================
#=================================== callback query =========================================
class Money(StatesGroup):
    get_val = State()

@dp.callback_query_handler(lambda c: c.data == "deposit")
async def callback_deposit(callback_query: types.CallbackQuery):
    markup = ReplyKeyboardMarkup()
    lang = await db.get_lang(callback_query.from_user.id)
    if lang == 'ru':
        markup.add(KeyboardButton("Назад"))
        text = "На какую суму хотите пополнить"
    elif lang == 'ua':
        text = "На яку суму хочете поповнити"
        markup.add(KeyboardButton("Назад"))
    elif lang == 'en':
        text = "How much do you want to deposit"
        markup.add(KeyboardButton("Back"))

    await bot.send_message(callback_query.from_user.id,text, reply_markup=markup)
    await Money.get_val.set()

@dp.message_handler(state=Money.get_val)
async def process_deposit(message: types.Message, state: FSMContext):
    global PayObj
    lang = await db.get_lang(message.from_user.id)
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        if user_message == "Back" or user_message == "Назад":
            await state.finish()
            await callback_back_main_menu(message)
            return None
        number = re.search(r'[0-9]+',user_message, re.I)
        if number != None:
            PayObj = Payments(message.from_user.id)
            url = await PayObj.get_form_url(number.group(),message.from_user.id)
            markup,text = await payments.keyboard(lang,url)
            await bot.send_message(message.from_user.id,text,reply_markup=markup)
            await state.finish()
            return None
        
@dp.callback_query_handler(lambda c: c.data == "check_pay")
async def process_check_payments(callback_query: types.CallbackQuery):
    global PayObj
    lang = await db.get_lang(callback_query.from_user.id)
    if lang == "ru":
        suctext = "Успешно пополнено"
        falltext = "Обрабатываеться"
    elif lang == "ua":
        suctext = "Успішно попвнено"
        falltext = "Обробка..."
    elif lang == "en":
        suctext = "Sucsessfull"
        falltext = "Loading..."
    payobj,amount = await PayObj.check_success_payment()
    if payobj:
        balance = await db.get_balance(callback_query.from_user.id)
        suma = balance + amount
        await db.change_balance(callback_query.from_user.id,suma)
        await bot.send_message(callback_query.from_user.id,suctext)

        return None
    else:
        await bot.send_message(callback_query.from_user.id,falltext)

        

class withdraw(StatesGroup):
    naeb = State()    

@dp.callback_query_handler(lambda c: c.data == "withdraw")
async def callback_withdraw(callback_query: types.CallbackQuery):
    lang = await db.get_lang(callback_query.from_user.id)
    markup = ReplyKeyboardMarkup()
    if lang == "ru":
        textmoney = "Введите сумму вывода"
        markup.add("Назад")
    elif lang == "ua":
        textmoney = "Введите сумму вывода"
        markup.add("Назад")
    elif lang == "en":
        textmoney = "Input sum for withdraw"
        markup.add("Back")
    
        
    await bot.send_message(callback_query.from_user.id,textmoney,reply_markup=markup)
    await withdraw.naeb.set()

@dp.message_handler(state=withdraw.naeb)
async def withdraw2(message: types.Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    if lang == "ru":
        text = "Введите номер карты"
    elif lang == "ua":
        text= "Введіть номер карти"
    elif lang == "en":
        text = "Input card number"
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        if user_message == "Back" or user_message == "Назад":
            await state.finish()
            await callback_back_main_menu(message)
            return None
        else:
            await state.finish()
            await bot.send_message(message.from_user.id,text)
        
        

#===========================================================================================


class GameDialog(StatesGroup):
    get_value = State()
    gtype = None

    

class Games():
    def __init__(self,lang,game_type,user_id):
        self.lang = lang
        self.game_type = game_type
        self.user_id = user_id
        

    async def casino_text(self):
        if self.lang == 'ru':
            rule = """
Сейчас выпадет случайное число от 1 до 99

Выберите исход события

< 50 - x2
= 50 - x10
> 50 - x2"""
            textfall = "💔 Вы проиграли!  Выпало число - {}"
            textwin = "❤️ Вы выиграли! Выпало число - {}"
            markup = ReplyKeyboardMarkup([[KeyboardButton("<50"),KeyboardButton("50"),KeyboardButton(">50")],[KeyboardButton("Назад")]])

        elif self.lang == 'ua':
            rule = """
Зараз випаде випадкове число від 1 до 99

Виберіть в яких межах знаходиться число 

< 50 - x2
= 50 - x10
> 50 - x2"""
            textfall = "💔 Ви програли! Випало число - {}"
            textwin = "❤️ Ви виграли! Ваше число - {}, число бота - {}"
            markup = ReplyKeyboardMarkup([[KeyboardButton("<50"),KeyboardButton("50"),KeyboardButton(">50")],[KeyboardButton("Назад")]])
            

        elif self.lang == 'en':
            rule = """
Now will drop random number 1 до 99

Please choose in which interval exist number 

< 50 - x2
= 50 - x10
> 50 - x2"""
            textfall = "💔 You lose! Number was - {}"
            textwin = "❤️ You win! Number was - {}"
            markup = ReplyKeyboardMarkup([[KeyboardButton("<50"),KeyboardButton("50"),KeyboardButton(">50")],[KeyboardButton("Back")]])
        
        return [textfall,textwin], [rule,markup]

    async def casino_key(self):
        _,d = await self.casino_text()
        await bot.send_message(self.user_id,d[0],reply_markup=d[1])

    
        
   
   # async def safe_text(self):
   #     pass

    async def dice_text(self):
        my_number = await bot.send_dice(self.user_id)
        bot_number = await bot.send_dice(self.user_id)
        if self.lang == 'ru':
            textfall = "💔 Вы проиграли! Ваше число - {}, число бота - {}"
            textwin = "❤️ Вы выиграли! Ваше число - {}, число бота - {}"
            texttie = "❤️ Ничья! Ваше число - {}, число бота - {}"
        elif self.lang == 'ua':
            textfall = "💔 Ви програли! Ваше число - {}, число бота - {}"
            textwin = "❤️ Ви виграли! Ваше число - {}, число бота - {}"
            texttie = "❤️ Ничія! Ваше число - {}, число бота - {}"
        elif self.lang == 'en':
            textfall = "💔 You lose! Your number - {}, Bot's number - {}"
            textwin = "❤️ You win! Your number - {}, Bot's number - {}"
            texttie = "❤️ Tie! Your number - {}, Bot's number - {}"
        return my_number.dice.value,bot_number.dice.value,[textfall,textwin,texttie]

    async def play_dice(self,balance):
        my,bots,text = await self.dice_text()
        if my < bots:
            await bot.send_message(self.user_id,text[0].format(my,bots))
            cash = self.u_balance - balance
            await db.change_balance(self.user_id,cash)
        elif my > bots:
            await bot.send_message(self.user_id,text[1].format(my,bots))
            cash = self.u_balance + balance
            await db.change_balance(self.user_id,cash)
        else:
            await bot.send_message(self.user_id,text[2].format(my,bots))

    async def play_casino(self,balance,predict):
        numb = random.randint(1,99)
        text, _ = await self.casino_text()
        if predict == "<50":
            if numb < 50:
                await bot.send_message(self.user_id,text[1].format(numb))
                cash = self.u_balance + (balance*2)
                await db.change_balance(self.user_id,cash)
            else:
                await bot.send_message(self.user_id,text[0].format(numb))
                cash = self.u_balance - balance
                if cash < 0: cash == 0
                await db.change_balance(self.user_id,cash)
        elif predict == ">50":
            if numb>50:
                await bot.send_message(self.user_id,text[1].format(numb))
                cash = self.u_balance + (balance*2)
                await db.change_balance(self.user_id,cash)
            else:
                await bot.send_message(self.user_id,text[0].format(numb))
                cash = self.u_balance - balance
                if cash < 0: cash == 0
                await db.change_balance(self.user_id,cash)
        elif predict == "50":
            if numb == 50:
                await bot.send_message(self.user_id,text[1].format(numb))
                cash = self.u_balance + (balance*10)
                await db.change_balance(self.user_id,cash)
            else:
                await bot.send_message(self.user_id,text[0].format(numb))
                cash = self.u_balance - balance
                if cash < 0: cash == 0
                await db.change_balance(self.user_id,cash)
        


    #async def play_safe(self,balance):
    #    pass #Доделать игру safe
        
        


    
    
    async def check_balance(self,balance):
        self.u_balance = int(await db.get_balance(self.user_id))
        if self.u_balance < balance:
            return True
            

    async def ErrorText2(self):
        if self.lang == "ru":
            return "Недостаточно средств"
        elif self.lang == "ua":
            return "Недостатньо коштів"
        elif self.lang == "en":
            return "Not enought cash"

    
    async def ErrorText(self):
        if self.lang == "ru":
            return "Пожалуйста введите суму"
        elif self.lang == "ua":
            return "Будь ласка введіть суму"
        elif self.lang == "en":
            return "Please input numbers"




#=============================== callback message game =====================================
@dp.message_handler(lambda c:  c.text.startswith("🎰"))
async def callback_game_casino(message: types.Message):
    lang = await db.get_lang(message.from_user.id)
    await GameDialog.get_value.set()
    GameDialog.gtype = "🎰"
    await bot.send_message(message.from_user.id,await Games(lang,None,None).ErrorText())


#@dp.message_handler(lambda c: c.text.startswith("📈"))
#async def callback_game_crash(message: types.Message):
#    lang = await db.get_lang(message.from_user.id)
#    await GameDialog.get_value.set()
#   GameDialog.gtype = "📈"
#    await bot.send_message(message.from_user.id,await Games(lang,None,None).ErrorText())

#@dp.message_handler(lambda c: c.text.startswith("🗄"))
#async def callback_game_safe(message: types.Message):
#    lang = await db.get_lang(message.from_user.id)
 #   await GameDialog.get_value.set()
 #   GameDialog.gtype = "🗄"
 #   await bot.send_message(message.from_user.id,await Games(lang,None,None).ErrorText())

@dp.message_handler(lambda c: c.text.startswith("🎲"))
async def callback_game_dice(message: types.Message):
    lang = await db.get_lang(message.from_user.id)
    await GameDialog.get_value.set()
    GameDialog.gtype = "🎲"
    await bot.send_message(message.from_user.id,await Games(lang,None,None).ErrorText())





@dp.message_handler(state=GameDialog.get_value)
async def process_games_dice(message: types.Message, state: FSMContext):
    global crash, t
    lang = await db.get_lang(message.from_user.id)
    GameObj = Games(lang,GameDialog.gtype,message.from_user.id)
    balance = await db.get_balance(message.from_user.id)

    
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        if user_message == "Back" or user_message == "Назад":
            await state.finish()
            await callback_back_main_menu(message)
            return None
        
        number = re.search(r'[0-9]+',user_message, re.I)
        if number == None:
            await bot.send_message(message.from_user.id,await GameObj.ErrorText())
        else:

            rate = float(number.group())
            
            if not await GameObj.check_balance(rate):
                
            
                if GameDialog.gtype == "🎲":
                    await GameObj.play_dice(rate)


                elif GameDialog.gtype == "🎰":
                    await GameObj.casino_key()
                    if user_message == "<50" or user_message =="50" or user_message ==">50":
                        await GameObj.play_casino(rate,user_message)
            else:
                await bot.send_message(message.from_user.id,await GameObj.ErrorText2())

#===========================================================================================
