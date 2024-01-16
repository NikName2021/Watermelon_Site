from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.dispatcher import FSMContext

from database.models import Appeals, Messages
from additional import *
from connection import *
from config import *
from crud import *


# @dp.message_handler(commands="answer")
# @dp.message_handler(Text(equals='Ответить'))
async def answer_key(message: types.Message):
    """
        Функция используется для вывода кнопок клавиатуры для оператора
    """
    if message.from_user.id in main_user.operators + main_user.admins:
        keyboard = await main_keyboard.operator_menu(message.from_user.id)
        await message.answer("""Команды оператора""", reply_markup=keyboard)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals='Активные обращения'))
async def active_appeals(message: types.Message):
    """
        Функция вывода обращений, которые ведет оператор
    """
    if message.from_user.id in main_user.operators + main_user.admins:
        self_user = await userRequests.get_user_telegram(message.from_user.id)
        appeals = await appealRequests.get_appeals_user(self_user.id)

        if not appeals:
            await message.answer("Нет активных обращений")
            return

        for appeal in appeals:
            await function.continue_appeal(message, appeal)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.callback_query_handler(main_filters.Ans())
async def op_pre_send(call: types.CallbackQuery, state: FSMContext):
    """
        Функция входа в машину ожидания сообщений для оператора
    """
    current_state = await state.get_state()
    if current_state:
        await call.message.answer("Вы находитесь в диалоге!!")
        return
    ida = call.data.split("-")
    app = await appealRequests.get_appeal(ida[1])
    self_user = await userRequests.get_user_telegram(call.from_user.id)

    if not app.status and (app.operator_id == None or app.operator_id == self_user.id):
        app.operator_id = self_user.id
        db.commit()

        async with state.proxy() as data:
            data["appeal"] = app.id
        await machine.MainOffer.mess.set()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text='Выйти из ожидания сообщений'))

        await call.message.answer("Введи сообщение", reply_markup=keyboard)
    elif app.status:
        await call.message.answer("Обращение уже удалено")
    else:
        await call.message.answer("У этого обращения уже есть оператор")


# @dp.message_handler(state=machine.MainOffer.mess)
async def op_main(message: types.Message, state: FSMContext):
    """
        Функция отправки сообщения оператора пользователю
    """
    async with state.proxy() as data:
        app_id = data["appeal"]

    app = await appealRequests.get_appeal(app_id)
    await messageRequests.message_create(app.id, message.text, True)
    typ = HElP_FOR_KEYBOARD[app.type]
    if not app.user_status:

        mes = f"""{message.text}
Для продолжения диалога нажми кнопку: 'Ответить'"""

        await bot.send_message(app.client_id, mes,
                               reply_markup=await inline_keybords.keyboard_to_client_send(app.id))
    else:
        await bot.send_message(app.client_id, message.text)


# @dp.callback_query_handler(main_filters.Archive())
async def archive_appeals(call: types.CallbackQuery):
    """
        Функция добавления обращения в архив
    """

    ida = call.data.split("-")
    app = db.query(Appeals).get(int(ida[1]))
    app.status = 2
    db.commit()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Обращение добавлено в архив")


def register_handler_operator(dp: Dispatcher):
    dp.register_message_handler(answer_key, Text(equals='Ответить'))
    dp.register_message_handler(answer_key, commands="answer")
    dp.register_message_handler(active_appeals, commands="aktiv_appels")
    dp.register_message_handler(active_appeals, Text(equals='Активные обращения'))
    dp.register_callback_query_handler(op_pre_send, main_filters.Ans())
    dp.register_callback_query_handler(archive_appeals, main_filters.Archive())
    dp.register_message_handler(op_main, state=machine.MainOffer.mess)
