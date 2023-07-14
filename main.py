from aiogram.client.session import aiohttp
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import reg_handlers, work_handlers, create_handlers
from settings.config import config
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage
# from redis.asyncio.client import Redis

async def main():

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(reg_handlers.router)
    dp.include_router(work_handlers.router)
    dp.include_router(create_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    # database = Database()
    # await database.connect()

async def save_photo(photo):
    bot = Bot(token=config.bot_token.get_secret_value())
    photo_file_id = photo.file_id
    photo_file = await bot.get_file(photo_file_id)
    # photo_data = await bot.download_file(photo_file)


    file_url = f"https://api.telegram.org/file/bot{config.bot_token.get_secret_value()}/{photo_file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                file_content = await response.read()

                # Теперь 'file_content' содержит содержимое файла в виде байтов
                return file_content
            else:
                print('Ошибка при получении файла')
                return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

