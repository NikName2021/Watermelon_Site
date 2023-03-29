from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.additional import *
from bot.connection import *
from aiogram import Dispatcher


# @dp.message_handler(Text(equals="Вернуться"))
# @dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    Данная функция используется для приветственной фразы и создания кнопок клавиатуры
    """

    if message.from_user.id in admins or message.from_user.id in operators:
        keyboard = await main_keyboard.start_ad_op(message.from_user.id)
    else:
        keyboard = await main_keyboard.user_keyboard()
    if message.text == "Вернуться":
        await message.answer("Привет!", reply_markup=keyboard)
    else:
        await message.answer('Привет! Я помогу тебе справиться со всеми переживаниями и проблемами.'
                             ' Давай определимся что случилось, для этого выбери пункт в меню ниже.',
                             reply_markup=keyboard)


async def help(message: types.Message):
    """
    Функция для вывода помощи(справки по командам) пользователю
    """
    await message.answer("""<b>Справка по командам бота.</b>
Возврат в главное меню, нажми /start""")


def register_handler_add(dp: Dispatcher):
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(help, Text(equals="Справка"))
    dp.register_message_handler(cmd_start, Text(equals="Вернуться"))
    dp.register_message_handler(cmd_start, commands="start")
