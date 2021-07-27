import asyncio

from aiohttp import web


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
#from aiogram.utils import context

from db import create_db

from config import TOKEN,WEBHOOK_PATH,WEBAPP_HOST,WEBAPP_PORT,WEBHOOK_URL




bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def startup(dispatcher: Dispatcher):
    await create_db()
    await bot.set_webhook(WEBHOOK_URL)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await bot.delete_webhook()


    


if __name__ == '__main__':
    from logic import dp
    #executor.start_polling(dp, on_shutdown=shutdown, on_startup=startup,skip_updates=True)

    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_PATH)
    app.on_startup.append(startup)
    #dp.loop.set_task_factory(context.task_factory)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)  # Heroku stores port you have to listen in your app
    