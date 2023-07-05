from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.reg_handlers import start_reg
from keyboards.reply_row import make_row_keyboard
from services.api import Api
from services.filters import ChangeFilter
from settings.database import Database, save_data_to_redis, get_data_from_redis, get_alldata_from_redis
from states.state import *

router = Router()


@router.message(F.text == 'Создание')
async def schema_apart(message: Message, state: FSMContext):
    await state.set_state(WorkPage.workspace)
    await message.answer(
        text=f"Выберите {CreatePage.list_create_text[0]}",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )

    await state.set_state(CreatePage.list_create_state[0])

@router.message()
async def all_state(message: Message, state: FSMContext):
    curr_state = await state.get_state()

    try:
        index = CreatePage.list_create_state.index(curr_state)
    except:
        index = 0

    await save_data_to_redis(str(curr_state).split(':')[-1], message.text)
    await save_data_to_redis('prev_state', curr_state)

    if index != len(CreatePage.list_create_state)-1:
        next_state_value = await next_state(curr_state)
        await state.set_state(next_state_value)
    else:
        await finish(message, state)
    curr_state = await state.get_state()

    state_attr = str(curr_state).split(':')[-1] + '_list'
    if hasattr(CreatePage, state_attr):
        attribute_value = getattr(CreatePage, state_attr)
        await message.answer(
            text=f"Выберите {CreatePage.list_create_text[index+1]}",
            reply_markup=make_row_keyboard(attribute_value)
        )

    else:
        try:
            await message.answer(
                text=f"Выберите {CreatePage.list_create_text[index+1]}",
                reply_markup=make_row_keyboard(prev_and_cancel)
            )
        except:
            pass






async def next_state(curr_state):
    index = CreatePage.list_create_state.index(curr_state)
    if index < len(CreatePage.list_create_state)-2:
        next_state_value = CreatePage.list_create_state[index+1]
    else:
        next_state_value = CreatePage.list_create_state[-1]
    return next_state_value


@router.message(CreatePage.finish)
async def finish(message: Message, state: FSMContext):
    state_list = [str(state).split("'")[1].split(':')[1] for state in CreatePage.list_create_state]
    data = await get_alldata_from_redis(state_list)
    print(data)
    await message.answer(
        f"Это ваше обьявление\n"
        f"Фото: {data['image_places']}\n"
        f"ЖК: {data['infrastructure_id']}\n"
        f"Этаж: {data['floor_id']}\n"
        f"Парадная: {data['riser_id']}\n"
        f"Комнаты: {data['quantity']}\n"
        f"Вид: {data['view_apart']}\n"
        f"Назначение: {data['appointment']}\n"
        f"Стейт: {data['apart_status']}\n"
        f"План: {data['plane']}\n"
        f"Площадь: {data['area']}\n"
        f"Кухня: {data['kitchen_area']}\n"
        f"Балкон: {data['balcony']}\n"
        f"Отопление: {data['heating']}\n"
        f"Платеж: {data['payment']}\n"
        f"Комиссия: {data['commission']}\n"
        f"Комуникации: {data['communication']}\n"
        f"Цена: {data['price']}\n"
        f"Схема: {data['schema_apart']}\n",
        reply_markup=make_row_keyboard(cancel_done)
    )
    await state.set_state(WorkPage.workspace)