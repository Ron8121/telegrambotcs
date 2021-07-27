import os





# откриваєш Телегу шукаєшь @BotFather, создаешь нового бота копируєш токен в кавички нижче

TOKEN = "1903114881:AAHPnaUsbGWxb-vu3r4cSrrZpT42ON5vBqw" #цей удалить

# пользовательське сооглашение пиши сам
RULES = "Пользовательське соглашение и т.д..."

# имя твого бота типо @BotMy 
BOT_NAME="@KOSMOLOT_WIN_Bot" 

# силка на челика из тех поддержки мож свою добавить типо @myname_123
SUPPORT_LINK = "@ONI_CHan"





# регайся на wayforpay.com создай магазин(сам розберешся) введеш данні і т.д.
# зайдеш в меню (Мои магазини/Настройки магазина) вибираєш свій магазин шукаєш пункт Реквизити магазина

# копіруєш значення MERCHANT LOGIN в MERCH_ID:

MERCH_API = "e98d1e....."
MERCH_ID = "freelance_user_......"

#советую разообраться с настройкой магазина и активировать так как изначально он в тестовом режиме тоесть если оплатить 
# товар то через 15 минут деньги вернуться но товар через бота уже будет показан!!!



# 1 регестрируйся на https://github.com/ 
# 2 создай репозиторий
# 3 перекинь туда всі файли з архіву
# 4 зарегестрируйся на heroku.com
# 5 создай нове приложения на цьом сайті
# 6 назви його і це названія встав сюди

HEROKU_APP_NAME = "telegrambotcs"

# 7 Deployment method вибери GitHub и встав названія репозиторія
# 8 ждеш поки за білдиться проект

# ГОТОВО!


# ============================== Не трогать ===========================================

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))


MERCH_BOT_URL = "https://t.me/{}".format(BOT_NAME[1:])
