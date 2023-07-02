from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def log_or_reg() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="login")
    kb.button(text="registration")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def share_location_button():
    share_location_button = types.KeyboardButton("Поделиться геолокацией", request_location=True)
    return share_location_button