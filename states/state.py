from aiogram.fsm.state import StatesGroup, State

prev_and_cancel = ["Назад", "Отмена"]
prev_cancel_done = ["Назад", "Отмена", 'Подтвердить']
reg_page = ["Вход", "Регистрация"]
log_page = ["Вход"]
second_page = ["Обьявления", "Создание", "Профиль", "Язык"]
list_profile = ['Mой профиль', 'Мои обьявления', 'Отмена']


class RegPage(StatesGroup):
    reg_or_auth = State()
    reg_email = State()
    reg_pass1 = State()
    reg_pass2 = State()
    reg_final = State()

    log_email = State()
    log_pass = State()

    list_reg_state = [reg_email, reg_pass1, reg_pass2]
    list_reg_text = ["Даваи попробуем зарегаться, введи имейл", "Введи пароль", "Повторите пароль"]
    list_log_state = [log_email, log_pass]


class WorkPage(StatesGroup):
    workspace = State()
    announcement_view = State()
    announcement_create = State()
    profile = State()

    my_profile = State()
    my_annoncement = State()

    list_workspace_state = [workspace, announcement_view, announcement_create, profile, my_profile, my_annoncement]
    list_workspace_text = ["Главный экран, Мои обьявления", "Создание обьялении", "Профиль"]


class CreatePage(StatesGroup):
    schema_apart = State()
    image_places = State()
    infrastructure_id = State()
    riser_id = State()
    floor_id = State()
    view_apart = State()
    technology = State()
    apart_status = State()
    quantity = State()
    appointment = State()
    state_apart = State()
    plane = State()
    area = State()
    kitchen_area = State()
    balcony = State()
    heating = State()
    payment = State()
    commission = State()
    communication = State()
    apart_description = State()
    price = State()

    list_create_state = [schema_apart, image_places, infrastructure_id, riser_id, floor_id, view_apart,
                         technology, apart_status, quantity, appointment, state_apart, plane,
                         area, kitchen_area, balcony, heating, payment, commission,
                         communication, apart_description, price]
    list_create_text = ['Схема_квартиры', 'Изображения', 'Идентификатор_инфраструктуры',
                        'Идентификатор_парадной', 'Идентификатор_этажа', 'Вид_квартиры',
                        'Технология', 'Статус_квартиры', 'Количество', 'Назначение', 'Состояние_квартиры', 'План',
                        'Площадь', 'Площадь_кухни', 'Балкон', 'Отопление', 'Оплата', 'Комиссия',
                        'Связь', 'Описание_квартиры', 'Цена']

    communication_list = ['Звонок', 'Сообщение', 'Звонок+Сообщение']
    view_list = ['Вторичное жилье', 'Новострой', 'Коттедж']
    technology_list = ['Панельный', 'Монолит']
    apart_status_list = ['Сдан', 'Не сдан']
    quantity_list = ['1-комнатная', '2-комнатная', '3-комнатная', '4-комнатная']
    appointment_list = ['Жилая', 'Коммерческая', 'Промышленная']
    state_list = ['Требует ремонта', 'Ремонт от строителей']
    balcony_list = ['Да', 'Нет']
    heating_list = ['Электрическое', 'Газовое']
    plane_list = ['Студия', 'Стандарт', 'Свободная', 'Пентхаус']
