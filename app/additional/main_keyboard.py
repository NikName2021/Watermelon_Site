from aiogram import types
from aiogram.types import KeyboardButton
from connection import main_user


async def user_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Послание дня"), types.KeyboardButton(text="Случайная цитата"))
    # button_3 = types.KeyboardButton(text="SOS! Мне нужна срочная помощь")
    button_4 = types.KeyboardButton(text="У меня есть вопрос")
    # button_5 = types.KeyboardButton(text="Есть предложение")
    # keyboard.add(button_3)
    keyboard.add(button_4)
    # keyboard.add(button_5)
    keyboard.add(KeyboardButton(text='Справка'))

    return keyboard


async def start_ad_op(message):
    button_2 = types.KeyboardButton(text="Послание дня")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_2, types.KeyboardButton(text="Случайная цитата"))

    if message in main_user.admins:
        keyboard.add(KeyboardButton(text='Ответить'),
                     KeyboardButton(text='Команды admin'))
    else:
        keyboard.add(KeyboardButton(text='Ответить'))

    return keyboard


async def admin_first():
    status = KeyboardButton(text="Статус обращения")
    add_operator = KeyboardButton(text="Добавить оператора")
    operators_and_admin = KeyboardButton(text='Просмотр операторов')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(status)
    keyboard.add(operators_and_admin, add_operator)
    keyboard.add(KeyboardButton(text="Вернуться"))

    return keyboard


async def operator_menu(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in main_user.admins:
        keyboard.add(KeyboardButton(text="Доступные обращения"))
    keyboard.add(KeyboardButton(text="Активные обращения"))
    keyboard.add(KeyboardButton(text="Вернуться"))

    return keyboard
