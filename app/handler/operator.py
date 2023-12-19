from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.dispatcher import FSMContext

from database.User import Appeals, Messages
from additional import *
from connection import *
from config import *


# @dp.message_handler(commands="answer")
# @dp.message_handler(Text(equals='Ответить'))
async def answer_key(message: types.Message):
    """
        Функция используется для вывода кнопок клавиатуры для оператора
    """
    if message.from_user.id in main_user.operators or message.from_user.id in main_user.admins:
        keyboard = await main_keyboard.operator_menu()
        await message.answer("""Команды оператора""", reply_markup=keyboard)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals=['Вопросы', 'Предложения', "Обращения"]))
async def operator_questions(message: types.Message):
    """
        Функция вывода доступных обращений из категорий ['Вопросы', 'Предложения', "Обращения"]
    """
    if message.from_user.id in main_user.operators or message.from_user.id in main_user.admins:
        app = db.query(Appeals).where(Appeals.type == TYPE_BELONG[message.text], Appeals.status == 0,
                                      Appeals.operator_id == None).all()
        if not app:
            await message.answer("Ничего не найдено")
            return
        for i in app:
            await function.send_add(message, i)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals='Активные обращения'))
async def aktiv_appels(message: types.Message):
    """
        Функция вывода обращений, которые ведет оператор
    """
    if message.from_user.id in main_user.operators or message.from_user.id in main_user.admins:
        i = db.query(User.id).where(User.telegram_id == message.from_user.id).first()[0]
        app = db.query(Appeals).where(Appeals.operator_id == i, Appeals.status == 0).all()

        if not app:
            await message.answer("Нет активных обращений")
            return

        for i in app:
            await function.contin(message, i)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals='Доступные обращения'))
async def freeappels(message: types.Message):
    """
        Функция используется для различных выводов доступных обращений для ответа
    """
    if message.from_user.id in main_user.operators or message.from_user.id in main_user.admins:
        app = db.query(Appeals).where(Appeals.status == 0,
                                      Appeals.operator_id == None).all()
        if not app:
            await message.answer("Ничего не найдено")
            return
        for i in app:
            await function.send_add(message, i)
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
    app = db.query(Appeals).get(int(ida[1]))
    i = db.query(User.id).where(User.telegram_id == call.from_user.id).first()[0]
    if not app.status and (app.operator_id == None or app.operator_id == i):
        app.operator_id = i
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
    app = db.query(Appeals).get(app_id)
    db.add(Messages(appeal_id=app.id, operator_type=True, text=message.text))
    db.commit()
    if not app.user_status:
        keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
            InlineKeyboardButton('Ответить', callback_data=f'main-{app.id}'))

        mes = f"""{message.text}
Для продолжения диалога нажми кнопку: 'Ответить'"""

        await bot.send_message(app.client_id, mes, reply_markup=keyboard_tc)
    else:
        await bot.send_message(app.client_id, message.text)


# @dp.callback_query_handler(main_filters.Dele())
async def del_appeals(call: types.CallbackQuery):
    """
        Функция удаления обращения из бд
    """

    ida = call.data.split("-")
    app = db.query(Appeals).get(int(ida[1]))
    i = db.query(User.id).where(User.telegram_id == call.from_user.id).first()[0]
    if not app.status and app.operator_id == None:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        app.status = 3
        db.commit()
        await call.message.answer("Обращение удалено")
    elif app.status:
        await call.message.answer(f"Данного обращения уже не существует")
    else:
        await call.message.answer(f"У этого обращения уже есть оператор")


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
    dp.register_message_handler(operator_questions, Text(equals=['Вопросы', 'Предложения', "Обращения"]))
    dp.register_message_handler(answer_key, Text(equals='Ответить'))
    dp.register_message_handler(answer_key, commands="answer")
    dp.register_message_handler(aktiv_appels, commands="aktiv_appels")
    dp.register_message_handler(aktiv_appels, Text(equals='Активные обращения'))
    dp.register_message_handler(freeappels, commands="appels_all")
    dp.register_message_handler(freeappels, Text(equals='Доступные обращения'))
    dp.register_callback_query_handler(op_pre_send, main_filters.Ans())
    dp.register_callback_query_handler(del_appeals, main_filters.Dele())
    dp.register_callback_query_handler(archive_appeals, main_filters.Archive())
    dp.register_message_handler(op_main, state=machine.MainOffer.mess)
