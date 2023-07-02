from aiogram.fsm.state import StatesGroup, State



prev_and_cancel = ["Назад", "Отмена"]
prev_cancel_done = ["Назад", "Отмена", 'Подтвердить']
reg_page = ["Вход", "Регистрация"]
log_page = ["Вход"]
second_page = ["Обьявления", "Создание", "Профиль", "Язык"]
list_profile = ['Mой профиль', 'Мои обьявления', 'Отмена']




class FirstPage(StatesGroup):
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



class SecondPage(StatesGroup):
    workspace = State()
    announcement_view = State()
    announcement_create = State()
    profile = State()

    my_profile = State()
    my_annoncement = State()

    list_workspace_state = [workspace, announcement_view, announcement_create, profile, my_profile, my_annoncement]
    list_workspace_text = ["Главный экран, Мои обьявления", "Создание обьялении", "Профиль"]



