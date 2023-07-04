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
    await message.answer(
        text=f"Выберите {CreatePage.list_create_text[0]}",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )

    await state.set_state(CreatePage.list_create_state[0])



@router.message()
async def all_state(message: Message, state: FSMContext):
    curr_state = await state.get_state()
    state_list = [str(state).split("'")[1].split(':')[1] for state in CreatePage.list_create_state]
    data = await get_alldata_from_redis(state_list)
    print(data)

    try:
        index = CreatePage.list_create_state.index(curr_state)
    except:
        index = 0


    state_attr = str(curr_state).split(':')[-1] + '_list'
    if hasattr(CreatePage, state_attr):

        attribute_value = getattr(CreatePage, state_attr)
        await message.answer(
            text=f"Выберите {CreatePage.list_create_text[index]}",
            reply_markup=make_row_keyboard(attribute_value)
        )
    else:
        await message.answer(
            text=f"Выберите {CreatePage.list_create_text[index]}",
            reply_markup=make_row_keyboard(prev_and_cancel)
        )

    await save_data_to_redis(str(curr_state).split(':')[-1], message.text)
    next_state_value = await next_state(curr_state)
    await state.set_state(next_state_value)

async def next_state(curr_state):
    index = CreatePage.list_create_state.index(curr_state)
    if index <= len(CreatePage.list_create_state)-2:
        next_state_value = CreatePage.list_create_state[index+1]
    else:
        next_state_value = CreatePage.list_create_state[-1]
    return next_state_value

@router.message(CreatePage.finish)
async def finish(message: Message, state: FSMContext):
    await message.answer(
        text="23435345",
        reply_markup=make_row_keyboard(cancel_done)
    )
    await state.set_state(WorkPage.workspace)