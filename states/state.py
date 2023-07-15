from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.i18n import gettext as _


prev_and_cancel = ["Назад", "Отмена"]
prev_cancel_done = ["Назад", "Отмена", 'Подтвердить']
cancel_edit_done = ["Отмена", "Изменить", 'Подтвердить']
reg_page = ["Вход", "Регистрация"]
log_page = ["Вход"]

prev_and_cancel_en = ["Back", "Cancel"]
prev_cancel_done_en = ["Back", "Cancel", 'Confirm']
cancel_edit_done_en = ["Cancel", "Edit", 'Confirm']
reg_page_en = ["Log In", "Registration"]
log_page_en = ["Log In"]

second_page = ["Обьявления", "Создание", "Профиль", "Язык"]
second_page_en = ["Ads", "Create", "Profile", "Language"]

list_profile = ['Mой профиль', 'Мои обьявления', 'Отмена']
list_profile_en =['My Profile', 'My Ads', 'Cancel']



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
    list_reg_text_en = ["Let's try to register, enter your email", "Enter your password", "Confirm your password"]
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
    list_workspace_text_en = ["Main screen, My ads", "Create ad", "Profile"]

class CreatePage(StatesGroup):
    all_state = State()
    schema_apart = State()
    images = State()
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
    price = State()
    location = State()
    finish = State()
    edit = State()
    image_places = State()


    # list_create_state = [schema_apart, images, image_places, infrastructure_id, riser_id, floor_id, ]
    # list_create_text = ['Схема_квартиры', 'Изображения', 'Размещение', 'Идентификатор_инфраструктуры',
    #                     'Идентификатор_парадной', 'Идентификатор_этажа']
    # list_create_text_en = ['Floor_plan', 'Images', 'Infrastructure_id', 'Staircase_id', 'Floor_id']

    list_create_state = [schema_apart, images, image_places, infrastructure_id, riser_id, floor_id, view_apart,
                         technology, apart_status, quantity, appointment, state_apart, plane,
                         area, kitchen_area, balcony, heating, payment, commission,
                         communication, price]
    list_create_text = ['Схема_квартиры', 'Изображения','Размещение', 'Идентификатор_инфраструктуры',
                        'Идентификатор_парадной', 'Идентификатор_этажа', 'Вид_квартиры',
                        'Технология', 'Статус_квартиры', 'Количество', 'Назначение', 'Состояние_квартиры', 'План',
                        'Площадь', 'Площадь_кухни', 'Балкон', 'Отопление', 'Оплата', 'Комиссия',
                        'Связь', 'Цена', 'Адрес']
    list_create_text_en = ['Apartment_Schema', 'Images', 'Place', 'Infrastructure_ID',
                           'Riser_ID', 'Floor_ID', 'Apartment_View',
                           'Technology', 'Apartment_Status', 'Quantity', 'Appointment', 'Apartment_State',
                           'Apartment_Plan',
                           'Area', 'Kitchen_Area', 'Balcony', 'Heating', 'Payment', 'Commission',
                           'Communication', 'Price', 'Address']

    communication_list = ['Звонок', 'Сообщение', 'Звонок+Сообщение']
    view_apart_list = ['Вторичное жилье', 'Новострой', 'Коттедж']
    technology_list = ['Панельный', 'Монолит']
    apart_status_list = ['Сдан', 'Не сдан']
    quantity_list = ['1-комнатная', '2-комнатная', '3-комнатная', '4-комнатная']
    appointment_list = ['Жилая', 'Коммерческая', 'Промышленная']
    state_apart_list = ['Требует ремонта', 'Ремонт от строителей']
    balcony_list = ['Да', 'Нет']
    heating_list = ['Электрическое', 'Газовое']
    plane_list = ['Студия', 'Стандарт', 'Свободная', 'Пентхаус']
    payment_list = ['Наличные', 'Мат. капитал', 'Ипотека', 'Военная ипотека', 'Неважно']

    payment_list_en = ['cash', 'maternity', 'mortgage', 'military', 'not']
    communication_list_en = ['Call', 'Message', 'Call+Message']
    view_apart_list_en = ['Secondary Housing', 'New Building', 'Cottage']
    technology_list_en = ['Panel', 'Monolithic']
    apart_status_list_en = ['Rented', 'Not Rented']
    quantity_list_en = ['1-room', '2-room', '3-room', '4-room']
    appointment_list_en = ['Residential', 'Commercial', 'Industrial']
    state_apart_list_en = ['Requires Repair', 'Repair from Builders']
    balcony_list_en = ['Yes', 'No']
    heating_list_en = ['Electric', 'Gas']
    plane_list_en = ['Studio', 'Standard', 'Free', 'Penthouse']