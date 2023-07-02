from aiogram.filters.callback_data import CallbackData


class ChangeFilter(CallbackData, prefix="change_filter"):
    text: str


