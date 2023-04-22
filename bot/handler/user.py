import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.additional import *
from bot.connection import *
from bot.config import *


# @dp.message_handler(Text(equals="Хочу получить послание дня"))
async def out_phrase(message: types.Message):
    """
    Функция для вывода фразы дня
    """
    mess = await function.get_phrase(message.from_user.id)
    await message.answer(f"""<b>Послание дня: </b>
{mess}""")


# @dp.message_handler(Text(equals='У меня есть вопрос'))
async def question(message: types.Message, state: FSMContext):
    await machine.Question.text.set()
    # вход в машину ожиданий сообщений пользователя
    async with state.proxy() as data:
        data["topic"] = TYPE[message.text]
    await message.answer(ANSWERS[TYPE[message.text]])


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
        db.add(app)
        db.flush()
        db.add(Messages(appeal_id=app.id, operator_type=False, text=message.text))
        db.commit()
        # for operator in operators:
        #     await function.mailing(message, operator, "Вопрос")
        # создание записи обращения в бд
    await state.finish()


def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(out_phrase, Text(equals="Хочу получить послание дня"))
    dp.register_message_handler(question, Text(
        equals=['У меня есть вопрос', 'SOS! Мне нужна срочная помощь', 'Есть предложение']))
    dp.register_message_handler(questions_send_mess, state=machine.Question.text)
