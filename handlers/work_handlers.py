from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.reg_handlers import start_reg
from keyboards.reply_row import make_row_keyboard
from services.api import Api
from services.filters import ChangeFilter
from settings.database import Database
from states.state import *

router = Router()


@router.message(F.text == 'Профиль')
async def workspace(message: Message, state: FSMContext):
    await message.answer(
        text="Это ваш профиль",
        reply_markup=make_row_keyboard(list_profile)
    )
    await state.set_state(WorkPage.my_profile)


@router.message(F.text == 'Mой профиль')
async def profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await Database.save_user(user_id=user_id, email=None, access_token=None,
                                         refresh_token=None)
    api = Api()
    get_something = await api.get_something(user_id, user_data.get('access_token'), user_data.get('refresh_token'),
                                            'api/auth/user/')
    if get_something:
        await message.answer(
            text=f"Это ваш профиль \n"
                 f"Имейл: {get_something['email']} \n"
                 f"Имя: {get_something['first_name']} \n"
                 f"Фамилия {get_something['last_name']}",
            reply_markup=make_row_keyboard(list_profile)
        )
        await state.set_state(WorkPage.my_annoncement)
    else:
        await message.answer(
            text='Refresh токен все, предеться вводить пароль',
            reply_markup=make_row_keyboard(log_page)
        )
        await start_reg(message, state)


@router.message(F.text == 'Мои обьявления')
async def annoncement(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await Database.save_user(user_id=user_id, email=None, access_token=None,
                                         refresh_token=None)

    api = Api()
    get_something = await api.get_something(user_id, user_data.get('access_token'), user_data.get('refresh_token'),
                                            'api/v1/apartment/my_apartment/')

    if get_something:
        print(get_something)
        await message.answer_photo(
            photo=get_something[0]['images'][0]['image'],
            caption=
            f"Это ваш профиль\n"
            f"Этаж: {get_something[0]['floor_id']['number']}\n"
            f"Парадная: {get_something[0]['riser_id']['number']}\n"
            f"Вид: {get_something[0]['view']}\n"
            f"Назначение: {get_something[0]['appointment']}\n"
            f"Стейт: {get_something[0]['state']}\n"
            f"План: {get_something[0]['plane']}\n"
            f"Площадь: {get_something[0]['area']}\n"
            f"Кухня: {get_something[0]['kitchen_area']}\n"
            f"Балкон: {get_something[0]['balcony']}\n"
            f"Отопление: {get_something[0]['heating']}\n"
            f"Платеж: {get_something[0]['payment']}\n"
            f"Комиссия: {get_something[0]['commission']}\n"
            f"Комуникации: {get_something[0]['communication']}\n"
            f"Цена: {get_something[0]['price']}\n"
            f"Схема: {get_something[0]['schema']}\n",
            reply_markup=make_row_keyboard(list_profile)
        )
    else:
        await message.answer(
            text='Скорее всего обьялений нет',
            reply_markup=make_row_keyboard(list_profile)
        )



@router.message(WorkPage.announcement_view)
@router.message(F.text == 'Обьявления')
async def annoncement_view(message: Message, state: FSMContext):

    if message.text == 'Обьявления':
        await state.update_data(iterator=None)
    data = await state.get_data()
    if data.get('user_id'):
        user_id = data.get('user_id')
    else:
        user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    user_data = await Database.save_user(user_id=user_id, email=None, access_token=None,
                                         refresh_token=None)
    api = Api()
    get_something = await api.get_something(user_id, user_data.get('access_token'), user_data.get('refresh_token'),
                                            'api/v1/apartment/')

    annoncement_buttons = InlineKeyboardBuilder()
    annoncement_buttons.add(types.InlineKeyboardButton(
        text="Предидущее",
        callback_data=ChangeFilter(text="prev_annoncement").pack())
    ).add(types.InlineKeyboardButton(
        text="Следующее",
        callback_data=ChangeFilter(text="next_annoncement").pack())
    ).add(types.InlineKeyboardButton(
        text="Геолокация",
        callback_data=ChangeFilter(text="geo").pack())
    )

    if get_something['results']:
        queryset = get_something['results']
        query_list = [i for i in range(0, len(queryset))]

        await message.answer(
            text='Нет ни одного объявления',
            reply_markup=make_row_keyboard(list_profile)
        )
        await state.update_data(max=max(query_list))
        data = await state.get_data()
        if data.get('iterator') == 0:
            i = data.get('iterator')
        else:
            i = max(query_list)
            await state.update_data(iterator=i)
        try:
            image = queryset[i]['images'][0]['image']
        except:
            image = 'https://netsh.pp.ua/wp-content/uploads/2017/08/Placeholder-1.png'
        image_url = image
        if data.get('iterator') == None:
            test = await message.answer_photo(
                photo=image_url,
                caption=
                f"Это последнее объявление\n"
                f"ЖК: {queryset[i]['infrastructure_id']}\n"
                f"Этаж: {queryset[i]['floor_id']['number']}\n"
                f"Парадная: {queryset[i]['riser_id']['number']}\n",
                reply_markup=annoncement_buttons.as_markup()
            )
        else:

            updated_photo_message = await message.edit_media(
                media=types.InputMediaPhoto(
                    media=image_url
                )
            )
            update_caption = await message.edit_caption(
                caption=
                f"Это последнее объявление\n"
                f"ЖК: {queryset[i]['infrastructure_id']}\n"
                f"Этаж: {queryset[i]['floor_id']['number']}\n"
                f"Парадная: {queryset[i]['riser_id']['number']}\n",
                reply_markup=annoncement_buttons.as_markup()
            )
    else:
        await message.answer(
        text = 'Нет записей в базе',
        reply_markup = make_row_keyboard(second_page)

        )
        # await start_reg(message, state)

@ router.callback_query(ChangeFilter.filter(F.text == "geo"))
async def show_location_callback(query: types.CallbackQuery):
# Отправка геолокации в ответ на нажатие кнопки
    await query.message.answer_location(latitude=51.5074, longitude=-0.1278)




@router.callback_query(ChangeFilter.filter(F.text == "prev_annoncement"))
async def prev_annoncement(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    i = data.get('iterator')
    if i > 0:
        i -= 1
        # print(i)
    await state.update_data(iterator=i)
    await annoncement_view(callback_query.message, state)


@router.callback_query(ChangeFilter.filter(F.text == "next_annoncement"))
async def next_annoncement(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    max_val = data.get('max')
    i = data.get('iterator')
    if i < max_val:
        i += 1
        await state.update_data(iterator=i)
        await annoncement_view(callback_query.message, state)
