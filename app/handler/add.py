from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from additional import *
from connection import *
from database.models import Appeals
from aiogram import Dispatcher


# @dp.message_handler(Text(equals="Вернуться"))
# @dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    Данная функция используется для приветственной фразы и создания кнопок клавиатуры
    """

    if message.from_user.id in main_user.admins + main_user.operators:
        keyboard = await main_keyboard.start_ad_op(message.from_user.id)
    else:
        keyboard = await main_keyboard.user_keyboard()

    if message.text == "Вернуться":
        await message.answer("Привет!", reply_markup=keyboard)
    else:
        await message.answer('Привет! Я помогу тебе справиться со всеми переживаниями и проблемами.'
                             ' Давай определимся что случилось, для этого выбери пункт в меню ниже.',
                             reply_markup=keyboard)

    if message.text == "/start" and message.from_user.id not in main_user.admins + main_user.operators:
        await message.answer("""Если у тебя случилось что-то серьезное, то нажми эту кнопку ⬇️.""",
                             reply_markup=await inline_keybords.SOS_kb())


# @dp.callback_query_handler(text="Out", state="*")
async def out_from_mc(call: types.CallbackQuery, state: FSMContext):
    """
        Функция выхода из ввода
         сообщений по завершению диалога для оператора
    """
    current_state = await state.get_state()
    if current_state is None:
        await call.message.answer("Еще не начат ввод даннных")
        return
    await state.finish()

    keyboard = await main_keyboard.start_ad_op(call.message.from_user.id)

    await call.message.answer("Ввод отменен", reply_markup=keyboard)


# @dp.message_handler(Text(equals="Выйти из ожидания сообщений"), state="*")
# @dp.message_handler(commands="cancel", state="*")
async def out_from(message: types.Message, state: FSMContext):
    """
        Функция выхода из ввода
         сообщений пользователям по их обращениям для оператора
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Еще не начат ввод данных")
        return
    await state.finish()
    if message.text == "Выйти из ожидания сообщений":
        if message.from_user.id in main_user.operators or message.from_user.id in main_user.admins:
            keyboard = await main_keyboard.start_ad_op(message.from_user.id)
        else:
            keyboard = await main_keyboard.user_keyboard()

        await message.answer("Ввод отменен", reply_markup=keyboard)
        return
    else:
        await message.answer("Ввод отменен")


# @dp.message_handler(Text(equals='Завершить разговор'), state="*")
async def end_conversation(message: types.Message, state: FSMContext):
    """
        Функция завершения диалога пользователя и оператора
    """
    keyboard = await main_keyboard.user_keyboard()
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Еще не начат ввод даннных")
        return
    else:
        try:
            async with state.proxy() as data:
                id_app = data["appeal"]
        except Exception:
            await message.answer("Надеемся, мы смогли вам помочь.", reply_markup=keyboard)
            return

    # создание клавиатуры для пользователя

    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Завершение', callback_data='Out'))
    # создание клавиатуры для выхода оператору
    app = db.query(Appeals).get(id_app)
    operator = db.query(User).get(app.operator_id)
    await function.end(operator.telegram_id, app.client_name, app.client_id, keyboard_tc)
    app.status = 1
    db.commit()
    await state.finish()

    await message.answer("Надеемся, мы смогли вам помочь", reply_markup=keyboard)


async def help(message: types.Message):
    """
    Функция для вывода помощи(справки по командам) пользователю
    """
    if message.from_user.id in main_user.operators:
        await message.answer("""<b>Справка по командам бота.</b>
/appels_all - вывести все доступные обращения
/answer - Клавиатура для оператора
/aktiv_appels - Активные обращения
/cancel - Отменить ввод данных пользователю
/start - Стартовое меню""")
    elif message.from_user.id in main_user.admins:
        await message.answer("""<b>Справка по командам бота.</b>""")
    else:
        await message.answer("""<b>Справка по командам бота.</b>
/quote - случайная цитата
/phrase - фраза дня
/cancel - Отменить ввод данных
/start - Стартовое меню""")


def register_handler_add(dp: Dispatcher):
    dp.register_message_handler(out_from, commands="cancel", state="*")
    dp.register_message_handler(out_from, Text(equals="Выйти из ожидания сообщений"), state="*")
    dp.register_message_handler(end_conversation, Text(equals=['Завершить разговор']), state="*")
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(help, Text(equals="Справка"))
    dp.register_callback_query_handler(out_from_mc, text="Out", state="*")
    dp.register_message_handler(cmd_start, Text(equals="Вернуться"))
    dp.register_message_handler(cmd_start, commands="start")
