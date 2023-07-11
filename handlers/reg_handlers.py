from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.reply_row import make_row_keyboard
from services.api import Api
from services.filters import ChangeFilter
from settings.database import Database, get_data_from_redis
from states.state import *

router = Router()

@router.message(Command("start"))
async def first_page_choose(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await Database.save_user(user_id=user_id, email=None, access_token=None, refresh_token=None)
    # api = Api()
    # get_something = api.get_something(user_id, user_data.get('access_token'), user_data.get('refresh_token'), 'api/auth/user/')


    if user_data and user_data.get('refresh_token'):
        await message.answer('Вы в базе есть', reply_markup=make_row_keyboard(second_page))
        await state.set_state(WorkPage.workspace)

    else:
        await message.answer('Вас не найдено, надо регистрироваться', reply_markup=make_row_keyboard(reg_page))
        await state.set_state(RegPage.reg_or_auth)





@router.message(RegPage.reg_or_auth, F.text == 'Регистрация')
async def start_reg(message: Message, state: FSMContext):
    await message.answer(
        text="Даваи попробуем зарегаться, введи имейл",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )
    await state.set_state(RegPage.list_reg_state[0])

@router.message(RegPage.reg_or_auth, F.text == 'Вход')
async def start_reg(message: Message, state: FSMContext):
    await message.answer(
        text="Введите имейл",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )
    await state.set_state(RegPage.list_log_state[0])

@router.message(F.text == 'Назад')
async def reg_prev(message: Message, state: FSMContext):
    user_data = await state.get_data()
    callback = user_data.get('callback')
    if callback:
        await state.update_data(callback='')

    curr_state = await state.get_state()
    if curr_state in WorkPage.list_workspace_state:
        index = WorkPage.list_workspace_state.index(curr_state)
        print(index)
        await message.answer(
            text="На главную",
            reply_markup=make_row_keyboard(second_page)
        )
        if index == 3 or 0:
            await state.set_state(WorkPage.list_workspace_state[0])
        else:
            await state.set_state(WorkPage.list_workspace_state[index - 1])
    elif curr_state in CreatePage.list_create_state:
        index = CreatePage.list_create_state.index(curr_state)
        if index == 0:
            await message.answer(
                text="Главная",
                reply_markup=make_row_keyboard(second_page)
            )
            await state.set_state(WorkPage.workspace)
        else:
            await message.answer(
                text=f"Выберите {CreatePage.list_create_text[index-1]}",
                reply_markup=make_row_keyboard(prev_and_cancel)
            )
            await state.set_state(CreatePage.list_create_state[index-1])


    elif curr_state not in RegPage.list_reg_state or curr_state == RegPage.list_reg_state[0]:
        # prev = await state.get_data()
        await message.answer(
            text="Шо опять!",
            reply_markup=make_row_keyboard(reg_page)
        )
        await state.set_state(RegPage.reg_or_auth)
    else:
        index = RegPage.list_reg_state.index(curr_state)
        print(index)
        prev = await state.get_data()
        await message.answer(
            text=RegPage.list_reg_text[index - 1],
            reply_markup=make_row_keyboard(prev_and_cancel)
        )
        await state.set_state(RegPage.list_reg_state[index - 1])

@router.message(F.text == 'Отмена')
async def reg_cancel(message: Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state in WorkPage.list_workspace_state or curr_state in CreatePage.list_create_state:
        await state.clear()
        await message.answer(
            text="И куда вас это привело. Снова ко мне!",
            reply_markup=make_row_keyboard(second_page)
        )
        await state.set_state(WorkPage.workspace)
    else:
        await state.clear()
        await message.answer(
            text="И куда вас это привело. Снова ко мне!",
            reply_markup=make_row_keyboard(reg_page)
        )
        await state.set_state(RegPage.reg_or_auth)

@router.message(RegPage.reg_or_auth)
async def choosen_incorrectly(message: Message):
    await message.answer(
        text="Или регистрация или смерть",
        reply_markup=make_row_keyboard(reg_page)
    )


@router.message(RegPage.reg_email)
async def reg_email_choosen(message: Message, state: FSMContext):
    current_text = "Введи имейл"
    await state.update_data(text=current_text)
    await state.update_data(reg_email=message.text)
    await message.answer(
        text="Введи пароль",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )
    await state.set_state(RegPage.reg_pass1)


@router.message(RegPage.reg_pass1)
async def reg_pass1_choosen(message: Message, state: FSMContext):
    current_text = "Введи пароль"
    await state.update_data(text=current_text)
    await state.update_data(reg_pass1=message.text)
    await message.answer(
        text="Повторите пароль",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )
    await state.set_state(RegPage.reg_pass2)


@router.message(RegPage.reg_pass2)
async def reg_pass2_chosen(message: Message, state: FSMContext):

    print(await state.get_state())
    current_text = "Повторите пароль"
    await state.update_data(text=current_text)
    if message.text != 'Подтвердить':
        user_data = await state.get_data()
        callback = user_data.get('callback')
        if callback == 'email':
            await state.update_data(reg_email=message.text)
        elif callback == 'pass1':
            await state.update_data(reg_pass1=message.text)
        elif callback == 'pass2':
            await state.update_data(reg_pass2=message.text)
        else:
            await state.update_data(reg_pass2=message.text)

    user_data = await state.get_data()
    email = user_data['reg_email']
    password1 = user_data['reg_pass1']
    password2 = user_data['reg_pass2']




    change_email = InlineKeyboardBuilder()
    change_email.add(types.InlineKeyboardButton(
        text="Изменить имейл",
        callback_data=ChangeFilter(text="change_email").pack())
    )
    change_pass1 = InlineKeyboardBuilder()
    change_pass1.add(types.InlineKeyboardButton(
        text="Изменить пароль",
        callback_data=ChangeFilter(text="change_pass1").pack())
    )
    change_pass2 = InlineKeyboardBuilder()
    change_pass2.add(types.InlineKeyboardButton(
        text="Изменить пароль",
        callback_data=ChangeFilter(text="change_pass2").pack())
    )

    await message.answer(
        text=f"Вы пытаетесь зарегаться под этими данными:\n"
             f"Имейл: {email}\n",
        reply_markup=change_email.as_markup(),
    )
    await message.answer(
        text=f"Пароль: {password1}\n",
        reply_markup=change_pass1.as_markup(),
    )
    await message.answer(
        text=f"Повторный пароль: {password2}",
        reply_markup=change_pass2.as_markup(),
    )
    await message.answer(
        text='Для регистрации нажминте подтвердить',
        reply_markup=make_row_keyboard(prev_cancel_done)
    )
    if message.text == 'Подтвердить':
        await process_registration(message, state)


async def process_registration(message: Message, state: FSMContext, db=None):
    user_data = await state.get_data()
    email = user_data['reg_email']
    password1 = user_data['reg_pass1']
    password2 = user_data['reg_pass2']

    api = Api()
    registration_result = api.registration(email, password1, password2)

    if registration_result is True:
        await message.answer(
            text=f"Вы зарегистрировались ваш имейл - {user_data['reg_email']}, подтвердите имейл на почте.",
            reply_markup=make_row_keyboard(log_page)
        )

        user_data = await Database.save_user(user_id=message.from_user.id, email=email,
                                             access_token=None, refresh_token=None)
        await state.set_state(RegPage.reg_or_auth)

    elif registration_result == 'email':
        await message.answer(
            text=f"Ошибочка вышла, имейл не прошел валидацию",
            reply_markup=make_row_keyboard(prev_and_cancel)
        )
        await state.set_state(RegPage.reg_final)
    elif registration_result == 'pass':
        await message.answer(
            text=f"Ошибочка вышла, Пароль не прошел валидацию",
            reply_markup=make_row_keyboard(prev_and_cancel)
        )
        await state.set_state(RegPage.reg_final)
    else:
        await message.answer(
            text=f"Ошибочка вышла, такой имейл уже есть в базе",
            reply_markup=make_row_keyboard(prev_and_cancel)
        )
        await state.set_state(RegPage.reg_final)




@router.callback_query(ChangeFilter.filter(F.text == "change_email"))
async def change_email(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(callback='email')
    await callback_query.answer()
    await callback_query.message.answer("Введите новый имейл")
    await state.set_state(RegPage.reg_pass2)

@router.callback_query(ChangeFilter.filter(F.text == "change_pass1"))
async def change_pass1(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(callback='pass1')
    await callback_query.answer()
    await callback_query.message.answer("Введите новый пароль")
    await state.set_state(RegPage.reg_pass2)

@router.callback_query(ChangeFilter.filter(F.text == "change_pass2"))
async def change_pass2(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(callback='pass2')
    await callback_query.answer()
    await callback_query.message.answer("Подтвердите новый пароль")
    await state.set_state(RegPage.reg_pass2)


@router.message(RegPage.log_email)
async def log_email_choosen(message: Message, state: FSMContext):
    current_text = "Введи имейл"
    await state.update_data(text=current_text)
    await state.update_data(log_email=message.text)
    await message.answer(
        text="Введите пароль",
        reply_markup=make_row_keyboard(prev_and_cancel)
    )
    await state.set_state(RegPage.log_pass)

@router.message(RegPage.log_pass)
async def log_pass_choosen(message: Message, state: FSMContext):
    current_text = "Введите пароль"
    await state.update_data(text=current_text)
    await state.update_data(log_pass=message.text)
    await message.answer(
        text="Вход",
        reply_markup=make_row_keyboard(log_page)
    )

    user_data = await state.get_data()
    email = user_data['log_email']
    password = user_data['log_pass']
    api = Api()
    authorization = api.authorization(email, password)
    if authorization is not False:
        data = authorization.json()
        print(data)
        access_token = data['access']
        refresh_token = data['refresh']
        user_data = await Database.save_user(user_id=message.from_user.id, email=email,
                                             access_token=access_token, refresh_token=refresh_token)
        await message.answer(
            text="Вход успешен",
            reply_markup=make_row_keyboard(second_page)
        )

        await state.set_state(WorkPage.workspace)