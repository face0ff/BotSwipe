from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData

from settings.database import get_data_from_redis
from states.state import CreatePage, WorkPage


class ChangeFilter(CallbackData, prefix="change_filter"):
    text: str


class StateCreateFilter(BaseFilter):
    async def __call__(self, message):
        prev_state = await get_data_from_redis('prev_state')
        try:
            state = str(prev_state).split(':')[1]
            print(state)
        except:
            return False

        if state == 'finish':
            return False
        else:
            return True