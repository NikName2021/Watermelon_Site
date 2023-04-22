
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.dispatcher import FSMContext, filters

from bot.additional import *
from bot.connection import *
from bot.config import *


# @dp.message_handler(commands="answer")
# @dp.message_handler(Text(equals='Ответить'))
async def answer_key(message: types.Message):
    """
        Функция используется для вывода кнопок клавиатуры для оператора
    """
    if message.from_user.id in operators or message.from_user.id in admins:
        keyboard = await main_keyboard.operator_menu()
        await message.answer("""Команды оператора""", reply_markup=keyboard)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals=['Вопросы', 'Предложения', "Обращения"]))
async def operator_questions(message: types.Message):
    """
        Функция вывода вопросов для админа
    """
    if message.from_user.id in operators or message.from_user.id in admins:
        app = db.query(Appeals).where(Appeals.type == TYPE_BELONG[message.text], Appeals.operator_id == None).all()
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
    if message.from_user.id in operators or message.from_user.id in admins:
        i = db.query(User.id).where(User.telegram_id == message.from_user.id).first()
        app = db.query(Appeals).where(Appeals.operator_id == i).all()

        if not app:
            await message.answer("Нет активных обращений")
            return

        for i in app:
            await function.contin(message, i)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(commands="appels_all")
# @dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['freeappels_([1-40]*)']))
# @dp.message_handler(Text(equals='Доступные обращения'))
async def freeappels(message: types.Message):
    """
        Функция используется для различных выводов доступных обращений для ответа
    """
    if message.from_user.id in operators or message.from_user.id in admins:
        if 'freeappels' in message.text:
            tx = int(message.text.split("_")[1])
            app = cur.execute("SELECT * FROM appels WHERE operator = 'No' ORDER BY date DESC").fetchall()[:tx]
        elif "appels_all" in message.text:
            app = cur.execute("SELECT * FROM appels WHERE operator = 'No' ORDER BY date DESC").fetchall()
        else:
            offers = cur.execute(f"SELECT * FROM offers WHERE operator = 'No'").fetchall()
            app = cur.execute("SELECT * FROM appels WHERE operator = 'No' ORDER BY date DESC").fetchall()
            questions = cur.execute(f"SELECT * FROM questions WHERE operator = 'No'").fetchall()

            if not app and not offers and not questions:
                await message.answer("Обращений нет")
                return

            for i in questions:
                await function.send_add(message, i, "Вопрос")
            for i in offers:
                await function.send_add(message, i, "Предложение")
        for i in app:
            await function.send_add(message, i, "Обращение")
    else:
        await message.answer("Нет прав на данную команду")


# @dp.callback_query_handler(main_filters.Ans())
async def op_pre_send(call: types.CallbackQuery, state: FSMContext):
    """
        Функция входа в машину ожидания сообщений для оператора
    """
    ida = call.data.split("-")
    sql = f"SELECT * FROM {main[ida[2]]} WHERE id = ?"
    check = cur.execute(sql, (int(ida[1]),)).fetchall()

    if check and (check[0][4] == "No" or check[0][4] == str(call.from_user.id)):
        sql_up = f'Update {main[ida[2]]} set operator = ? where id = ?'
        cur.execute(sql_up, (call.from_user.id, ida[1]))
        con.commit()

        async with state.proxy() as data:
            data["id"] = ida[1]
            data['typ'] = main[ida[2]]
        await machine.MainOffer.mess.set()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text='Выйти из ожидания сообщений'))

        await call.message.answer("Введи сообщение", reply_markup=keyboard)
    elif not check:
        await call.message.answer("Обращение уже удалено")
    else:
        await call.message.answer("У этого обращения уже есть оператор")


# @dp.message_handler(state=machine.MainOffer.mess)
async def op_main(message: types.Message, state: FSMContext):
    """
        Функция отправки сообщения оператора пользователю
    """
    async with state.proxy() as data:
        ids = data["id"]
        typ = data["typ"]
    sql = f"SELECT * FROM {typ} WHERE id = ?"
    check = cur.execute(sql, (str(ids),)).fetchall()
    if check[0][5] == "No":
        keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
            InlineKeyboardButton('Ответить', callback_data=f'main-{typ}-{check[0][4]}-{ids}'))

        mes = f"""{message.text}
Для продолжения диалога нажми кнопку: 'Ответить'"""

        await bot.send_message(ids, mes, reply_markup=keyboard_tc)
    else:
        await bot.send_message(ids, message.text)


# @dp.message_handler(state=machine.Opearator.mess)
async def op_send_message(message: types.Message, state: FSMContext):
    """
        Функция отправки сообщения оператора пользователю
    """
    async with state.proxy() as data:
        ids = data["id"]
    await bot.send_message(ids, message.text)


# @dp.callback_query_handler(main_filters.Dele())
async def del_appels(call: types.CallbackQuery):
    """
        Функция удаления обращения из бд
    """

    ida = call.data.split("-")
    sql = f"SELECT * FROM {main[ida[2]]} WHERE id = ?"
    check = cur.execute(sql, (ida[1],)).fetchall()
    if check and check[0][5] != "No":
        await call.message.answer(f"У этого {ida[2]} уже есть оператор")
    elif not check:
        await call.message.answer(f"Такого {ida[2]} уже не существует")
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        sqldel = f"DELETE FROM {main[ida[2]]} WHERE id = ?"
        cur.execute(sqldel, (ida[1],))
        con.commit()
        await call.message.answer("Обращение удалено")


# @dp.callback_query_handler(main_filters.Archive())
async def archive_appels(call: types.CallbackQuery):
    """
        Функция добавления обращения в архив
    """

    ida = call.data.split("-")

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    sql_up = f'Update {main[ida[2]]} set archive = ? where id = ?'
    cur.execute(sql_up, ("Yes", ida[1]))
    con.commit()
    await call.message.answer("Обращение добавлено в архив")


# @dp.message_handler(commands="help_operator")
async def help_operator(message: types.Message):
    """
        Функция используется для вывода помощи оператору
    """
    if message.from_user.id in operators or message.from_user.id in admins:
        await message.answer("""/appels_all - вывести все доступные обращения
/freeappels_[1-40] - вывести желаемое количество доступных обращений
/questions - вывести вопросы пользователей(также можно написать боту "Вопросы")
/offers - вывести вопросы пользователей(также можно написать боту "Предложения")
/main_offers - диалог с пользователем насчет предложения(также можно написать боту "Предложения в моей работе")""")
    else:
        await message.answer("Нет прав на данную команду")


def register_handler_operator(dp: Dispatcher):
    dp.register_message_handler(operator_questions, Text(equals=['Вопросы', 'Предложения', "Обращения"]))

    # dp.register_callback_query_handler(del_offers, main_filters.Off_del())
    # dp.register_callback_query_handler(del_question, main_filters.Que())
    # dp.register_callback_query_handler(set_offer, main_filters.Off_main())

    dp.register_message_handler(answer_key, Text(equals='Ответить'))
    dp.register_message_handler(answer_key, commands="answer")
    #
    # dp.register_message_handler(aktiv_offers, commands="main_offers")
    # dp.register_message_handler(aktiv_offers, Text(equals='Предложения в моей работе'))
    #
    # dp.register_message_handler(aktiv_appels, Text(equals='Активные обращения'))
    #
    # dp.register_message_handler(freeappels, commands="appels_all")
    # dp.register_message_handler(freeappels, filters.RegexpCommandsFilter(regexp_commands=['freeappels_([1-40]*)']))
    # dp.register_message_handler(freeappels, Text(equals='Доступные обращения'))
    #
    # dp.register_callback_query_handler(op_pre_send, main_filters.Ans())
    # dp.register_callback_query_handler(del_appels, main_filters.Dele())
    # dp.register_callback_query_handler(archive_appels, main_filters.Archive())
    #
    # dp.register_message_handler(op_main, state=machine.MainOffer.mess)
    # dp.register_message_handler(op_send_message, state=machine.Opearator.mess)
    #
    # dp.register_message_handler(help_operator, commands="help_operator")