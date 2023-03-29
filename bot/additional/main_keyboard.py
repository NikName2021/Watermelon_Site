from aiogram import types
from aiogram.types import KeyboardButton
from bot.connection import admins


async def user_keyboard():
    button_2 = types.KeyboardButton(text="Хочу получить послание дня")
    button_3 = types.KeyboardButton(text="SOS! Мне нужна срочная помощь")
    button_4 = types.KeyboardButton(text="У меня есть вопрос")
    button_5 = types.KeyboardButton(text="Есть предложение")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_2)
    keyboard.add(button_3)
    keyboard.add(button_4)
    keyboard.add(button_5)
    keyboard.add(KeyboardButton(text='Справка'))

    return keyboard


async def start_ad_op(message):
    button_2 = types.KeyboardButton(text="Хочу получить послание дня")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_2)

    if message in admins:
        keyboard.add(KeyboardButton(text='Ответить'),
                     KeyboardButton(text='Команды admin'))
    else:
        keyboard.add(KeyboardButton(text='Ответить'))

    return keyboard


async def admin_first():
    add_admin = KeyboardButton(text="Добавить админа")
    add_operator = KeyboardButton(text="Добавить оператора")
    operators_and_admin = KeyboardButton(text='Просмотр админов и операторов')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(add_admin, add_operator)
    keyboard.add(operators_and_admin)
    keyboard.add(KeyboardButton(text="Вернуться"))

    return keyboard


async def operator_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Доступные обращения"))
    keyboard.add(KeyboardButton(text="Активные обращения"))
    keyboard.add(KeyboardButton(text="Вернуться"))

    return keyboard