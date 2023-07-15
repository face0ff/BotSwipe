import os

from aiogram.client.session import aiohttp
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

from handlers import reg_handlers, work_handlers, create_handlers
from midlwares.locales import MyI18nMiddleware
from settings.config import config, LOCALES_DIR, DOMAIN
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
import locales
# from aiogram.fsm.storage.redis import RedisStorage
# from redis.asyncio.client import Redis

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())

async def main():

    logging.basicConfig(level=logging.INFO)
    i18n = I18n(path=LOCALES_DIR, default_locale="ru", domain=DOMAIN)
    dp.message.outer_middleware(MyI18nMiddleware(i18n=i18n))
    dp.callback_query.outer_middleware(MyI18nMiddleware(i18n=i18n))

    dp.include_router(reg_handlers.router)
    dp.include_router(work_handlers.router)
    dp.include_router(create_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def photo_url(photo):
    photo_file_id = photo.file_id
    photo_file_url = await bot.get_file(photo_file_id)
    return photo_file_url.file_id

async def save_photo(photo):
    photo_file = await bot.download(photo)
    return photo_file

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

