import io

from aiogram import Router, F, types
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.reg_handlers import start_reg
from keyboards.reply_row import make_row_keyboard, make_row_five_keyboard
from main import save_photo, photo_url
from services.api import Api
from services.filters import ChangeFilter, StateCreateFilter
from services.location_to_addess import get_address_from_coordinates
from settings.database import Database, save_data_to_redis, get_data_from_redis, get_alldata_from_redis, \
    save_apart_to_redis
from states.state import *
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

router = Router()

@router.message(F.text == 'Create')
@router.message(F.text == 'Создание')
async def schema_apart(message: Message, state: FSMContext):
    await state.set_state(WorkPage.workspace)
    await message.answer(
        text=_("Выберите {text}").format(text=CreatePage.list_create_text[0]),
        reply_markup=make_row_keyboard(prev_and_cancel if await get_data_from_redis('lang') == 'ru' else prev_and_cancel_en)
    )
    curr_state = await state.get_state()
    await save_data_to_redis('prev_state', curr_state)
    await state.set_state(CreatePage.list_create_state[0])


@router.message(CreatePage.edit)
async def apart_edit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await Database.save_user(user_id=user_id, email=None, access_token=None,
                                         refresh_token=None)
    api = Api()
    print("apart_edit")
    curr_state = await state.get_state()
    await save_data_to_redis('prev_state', curr_state)
    if message.text == _("Изменить"):
        await message.answer(
            text=_("Тут вы можете изменить ранее введенные данные"),
            reply_markup=make_row_five_keyboard(CreatePage.list_create_text if await get_data_from_redis('lang') == 'ru' else CreatePage.list_create_text_en)
        )
        # await state.set_state(CreatePage.edit)
    elif message.text == _("Подтвердить"):
        await message.answer(
            text=_("Супер объявление отправлено на модерацию"),
            reply_markup=make_row_keyboard(second_page if await get_data_from_redis('lang') == 'ru' else second_page_en)
        )
        state_list = [str(state).split("'")[1].split(':')[1] for state in CreatePage.list_create_state]
        data = await get_alldata_from_redis(state_list)
        address = await get_data_from_redis('location')
        photo_img = await save_photo(data['images'])
        photo_schema = await save_photo(data['schema_apart'])
        print(data)


        form_data = aiohttp.FormData()
        form_data.add_field('image_places', str(data['image_places']))
        form_data.add_field('images', photo_img, filename='images.jpg')
        form_data.add_field('schema', photo_schema, filename='schema.jpg')
        form_data.add_field('infrastructure_id', str(data['infrastructure_id']))
        form_data.add_field('riser_id', str(data['riser_id']))
        form_data.add_field('floor_id', str(data['floor_id']))
        form_data.add_field('view', str(data['view_apart']))
        form_data.add_field('technology', str(data['technology']))
        form_data.add_field('apart_status', str(data['apart_status']))
        form_data.add_field('quantity', str(data['quantity']))
        form_data.add_field('appointment', str(data['appointment']))
        form_data.add_field('state', str(data['state_apart']))
        form_data.add_field('plane', str(data['plane']))
        form_data.add_field('area', str(data['area']))
        form_data.add_field('kitchen_area', str(data['kitchen_area']))
        form_data.add_field('balcony', str(data['balcony']))
        form_data.add_field('heating', str(data['heating']))
        form_data.add_field('payment', str(data['payment']))
        form_data.add_field('communication', str(data['communication']))
        form_data.add_field('commission', str(data['commission']))
        form_data.add_field('apart_description', str(address))
        form_data.add_field('price', str(data['price']))

        await api.save_something(user_id, user_data.get('access_token'), user_data.get('refresh_token'),
                                 'api/v1/apartment/', form_data)

        await state.clear()


    else:
        print('22222')
        index = CreatePage.list_create_text.index(message.text)
        print(index)
        print(CreatePage.list_create_text[index])
        try:
            await state.set_state(CreatePage.list_create_state[index])
            await message.answer(
                text=CreatePage.list_create_text[index],
                reply_markup=make_row_five_keyboard(CreatePage.list_create_text if await get_data_from_redis('lang') == 'ru' else CreatePage.list_create_text_en)
            )
            await state.set_state(CreatePage.list_create_state[index])
        except:
            await state.set_state(CreatePage.location)


@router.message(F.text == 'Адрес')
@router.message(CreatePage.location)
async def location(message: Message, state: FSMContext):
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        address = await get_address_from_coordinates(latitude, longitude)
        curr_state = await state.get_state()
        await save_data_to_redis(str(curr_state).split(':')[-1], address)
        await message.answer(
            text=_("Спасибо огонь"),
            reply_markup=make_row_keyboard(prev_and_cancel if await get_data_from_redis('lang') == 'ru' else prev_and_cancel_en)
        )
    else:
        await message.answer(
            text=_("Выберите локацию"),
            reply_markup=make_row_keyboard(prev_and_cancel if await get_data_from_redis('lang') == 'ru' else prev_and_cancel_en)
        )
        return

    await finish(message, state)

@router.message(F.text == 'Language')
@router.message(F.text == 'Язык')
async def change_language(message: Message, state: FSMContext):
    current_language = await get_data_from_redis('lang')
    new_language = "en" if current_language == "ru" else "ru"
    await save_data_to_redis('lang', new_language)
    await message.answer(_("Язык изменен на {new_language}".format(new_language=new_language)),
                         reply_markup=make_row_keyboard(
                             second_page if await get_data_from_redis('lang') == 'ru' else second_page_en))


@router.message(StateCreateFilter())
async def all_state(message: Message, state: FSMContext):
    print("all_state")
    curr_state = await state.get_state()
    try:
        index = CreatePage.list_create_state.index(curr_state)
    except:
        index = 0
    if message.photo:
        photo = message.photo[-1]
        # photo_file = await save_photo(photo)
        # print(photo_file)
        photo_file_url = await photo_url(photo)
        # photo_download_url = await photo_download(photo)
        # print(photo_download_url)
        await save_apart_to_redis(str(curr_state).split(':')[-1], photo_file_url)
        await save_apart_to_redis('url', photo_file_url)
    else:
        await save_data_to_redis(str(curr_state).split(':')[-1], message.text)
    prev_state = await get_data_from_redis('prev_state')
    edit = str(prev_state).split(':')[1]
    print(edit)

    if edit == "edit":
        print('зашли сюда, выбираем финиш')
        await state.set_state(CreatePage.finish)
        await finish(message, state)
    elif index != len(CreatePage.list_create_state) - 1:
        # await save_data_to_redis('prev_state', curr_state)
        next_state_value = await next_state(curr_state)
        await state.set_state(next_state_value)
        curr_state = await state.get_state()
        state_attr = str(curr_state).split(':')[-1] + '_list'
        if hasattr(CreatePage, state_attr):
            attribute_value = getattr(CreatePage, state_attr)
            await message.answer(
                text=_("Выберите {text}").format(text=CreatePage.list_create_text[index + 1]),
                reply_markup=make_row_keyboard(attribute_value)
            )

        else:
            try:
                await message.answer(
                    text=_("Выберите {text}").format(text=CreatePage.list_create_text[index + 1]),
                    reply_markup=make_row_keyboard(prev_and_cancel if await get_data_from_redis('lang') == 'ru' else prev_and_cancel_en)
                )
            except:
                pass
    else:
        await message.answer(
            text=_("Выберите локацию"),
            reply_markup=make_row_keyboard(prev_and_cancel if await get_data_from_redis('lang') == 'ru' else prev_and_cancel_en)
        )
        await state.set_state(CreatePage.location)


async def next_state(curr_state):
    print("next_state")
    index = CreatePage.list_create_state.index(curr_state)
    if index < len(CreatePage.list_create_state) - 2:
        next_state_value = CreatePage.list_create_state[index + 1]
    else:
        next_state_value = CreatePage.list_create_state[-1]
    return next_state_value


@router.message(CreatePage.finish)
async def finish(message: Message, state: FSMContext):
    print("finish")
    # await set_location(message)
    state_list = [str(state).split("'")[1].split(':')[1] for state in CreatePage.list_create_state]
    data = await get_alldata_from_redis(state_list)
    address = await get_data_from_redis('location')
    url = await get_data_from_redis('url')

    await message.answer_photo(
        photo=data['images'],
        caption=
        f"Это ваше объявление\n"
        f"ЖК: {data['infrastructure_id']}\n"
        f"Этаж: {data['floor_id']}\n"
        f"Парадная: {data['riser_id']}\n"
        f"Локация: {address}\n"
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
        f"Коммуникации: {data['communication']}\n"
        f"Цена: {data['price']}\n"
        f"Схема: {url}\n"
        ,
        reply_markup=make_row_keyboard(
            cancel_edit_done if await get_data_from_redis('lang') == 'ru' else cancel_edit_done_en)
    )
    await state.set_state(CreatePage.edit)
    print('konec')
