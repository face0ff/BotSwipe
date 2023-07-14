from typing import Dict, Any

from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message
from aiogram.utils.i18n import I18nMiddleware

from settings.database import get_data_from_redis, save_data_to_redis


class MyI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        try:
            current_language = await get_data_from_redis('lang')
        except:
            current_language = 'ru'
            await save_data_to_redis('lang', current_language)
        return current_language
