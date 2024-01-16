import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton
from database.models import Appeals, Messages
from additional import *
from connection import *
from config import *
from crud.userRequests import *
from crud.messageRequests import *
from crud.appealRequests import *


# @dp.message_handler(Text(equals="Послание дня"))
async def out_phrase(message: types.Message):
    """
    Функция для вывода фразы дня
    """
    mess = await function.get_phrase(message.from_user.id)
    await message.answer(f"""<b>Послание дня: </b>
{mess}""")


# @dp.message_handler(Text(equals="Случайная цитата"))
async def random_quote(message: types.Message):
    """
    Функция для вывода случайной цитаты из api.forismatic.com
    """
    page = requests.post('http://api.forismatic.com/api/1.0/?method=getQuote&lang=ru&format=json')
    page = page.json()
    await message.answer(f"""<b>Случайная цитата: </b>
{page['quoteText']}
<b>{page['quoteAuthor']}</b>""")


# @dp.message_handler(Text(equals='У меня есть вопрос'))
async def question(message: types.Message, state: FSMContext):
    await machine.Question.text.set()
    # вход в машину ожиданий сообщений пользователя
    async with state.proxy() as data:
        data["topic"] = TYPE[message.text]
    await message.answer(ANSWERS[TYPE[message.text]])


# @dp.message_handler(Text(equals='У меня есть вопрос'))
async def question_call(call: types.CallbackQuery, state: FSMContext):
    await machine.Question.text.set()
    # вход в машину ожиданий сообщений пользователя
    async with state.proxy() as data:
        data["topic"] = 3
    await call.message.answer(ANSWERS[3])


# @dp.message_handler(state=machine.Question.text)
async def questions_send_mess(message: types.Message, state: FSMContext):
    """
    Функция фильтрации и распределения сообщения пользователя
    """
    check = await function.check_filter(message)
    if check == 1:
        # если в сообщении найден мат
        await message.answer("Выражайся культурнее. Перефразируй свое сообщение")
        await asyncio.sleep(1)

    if message.text in ('Хочу получить послание дня',
                        'У меня есть вопрос', 'Есть предложение', 'SOS! Мне нужна срочная помощь', 'Справка'):
        # если сообщение равно кнопке
        await message.answer("Ваше сообщение не отправлено, попробуй снова")
        await asyncio.sleep(1)
    else:
        keyboard = await main_keyboard.user_keyboard()
        async with state.proxy() as data:
            topic = data["topic"]

        await message.answer(ANSWERS_FINAL[topic], reply_markup=keyboard)
        app = Appeals(client_id=message.from_user.id, client_name=message.from_user.full_name, type=topic, status=0)
        # создание записи обращения в бд
        db.add(app)
        db.flush()
        db.add(Messages(appeal_id=app.id, operator_type=False, text=message.text))
        db.commit()

        for admin in main_user.admins:
            await function.mailing_for_sorting(message, admin, app)
            # отправка операторам

    await state.finish()


# @dp.callback_query_handler(text="main")
async def beginning(call: types.CallbackQuery, state: FSMContext):
    """
    Функция фильтрации и распределения сообщения пользователя
    """

    ida = call.data.split("-")
    await machine.AnswerOffers.text.set()
    app = db.query(Appeals).get(int(ida[1]))
    app.user_status = True
    db.commit()
    async with state.proxy() as data:
        data["appeal"] = ida[1]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=f"Завершить разговор"))

    await call.message.answer("Ваши сообщения будут отправлены оператору", reply_markup=keyboard)


# @dp.message_handler(state=machine.AnswerOffers.text)
async def user_send_mess(message: types.Message, state: FSMContext):
    # отправка сообщения напрямую оператору

    async with state.proxy() as data:
        id_app = data["appeal"]
    await message_create(id_app, message.text, False)

    appeal = await get_appeal(id_app)
    await set_status(appeal, STATUS['work'])
    operator = await get_user(appeal.operator_id)

    await bot.send_message(operator.telegram_id, f"""Сообщение по {MESS_ABOUT[appeal.type]} от {
    appeal.client_name} - |**{str(appeal.client_id)[6:]}|
{message.text}""")


def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(out_phrase, commands="phrase")
    dp.register_message_handler(out_phrase, Text(equals="Послание дня"))
    dp.register_message_handler(random_quote, commands="quote")
    dp.register_message_handler(random_quote, Text(equals="Случайная цитата"))
    dp.register_callback_query_handler(question_call, text="help_keyboard")
    dp.register_message_handler(question, Text(
        equals=['У меня есть вопрос', 'SOS! Мне нужна срочная помощь', 'Есть предложение']))
    dp.register_message_handler(questions_send_mess, state=machine.Question.text)
    dp.register_callback_query_handler(beginning, main_filters.Main())
    dp.register_message_handler(user_send_mess, state=machine.AnswerOffers.text)
