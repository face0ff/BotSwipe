from aiogram.fsm.storage.memory import MemoryStorage

from handlers import reg_handlers, work_handlers, create_handlers
from settings.config import config
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

