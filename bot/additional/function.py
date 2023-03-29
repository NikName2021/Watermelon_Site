import datetime
import re
from random import choice

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import *
from bot.connection import *


async def varible():

    """Функция обновления данных из бд
    после добавления нового админа или оператора"""

    global admins
    global operators
    operators = [i[0] for i in cur.execute(f"SELECT * FROM user").fetchall() if "operator" in i[2].split()]
    admins = [i[0] for i in cur.execute(f"SELECT * FROM user").fetchall() if "admin" in i[2].split()]


async def get_phrase(user_id):

    """Функция формирования фразы дня"""

    checks = cur.execute(f"SELECT * FROM phrase WHERE id = ?", (user_id,)).fetchall()
    if not bool(checks):
        phrase = choice(EVERYDAY)
        cur.execute(f"INSERT INTO phrase VALUES (?, ?, ?)", (user_id, phrase, datetime.date.today()))
        con.commit()
        return phrase

    else:
        checks = checks[0]
        if checks[2] == str(datetime.date.today()):
            return checks[1].split('; ')[-1]
        else:
            phrases = checks[1].split('; ')
            if len(phrases) == 7:
                phrases = []
            phrase = choice(EVERYDAY)
            while phrase in phrases:
                phrase = choice(EVERYDAY)
            phrases.append(phrase)
            cur.execute(f'Update phrase set phrases = ?, date = ?  where id = {checks[0]}',
                        ("; ".join(phrases), datetime.date.today()))
            con.commit()
            return phrase


async def f(s):
    urls = re.findall(r'http(?:s)?://\S+', s)
    return len(urls) != 0


async def check_filter(mess):
    """ Функция проверки сообщений"""
    words = mess.text.split()
    for word in words:
        if str.lower(word) in NO_CENSORED or await f(str.lower(word)):
            # await bot.delete_message(mess.chat.id, mess.message_id)
            return 1


async def send_add(message, i, typ):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'ans-{i[1]}-{typ}')).add(
        InlineKeyboardButton('Удалить', callback_data=f'del-{i[1]}-{typ}'))

    if typ == "Обращение":
        typ = "⛔️⛔️🛑🆘🆘🆘❌❌Обращение⛔️⛔️🛑🆘🆘🆘❌❌"

    await message.answer(f"""<b>{typ}</b>
<b>Отправитель:</b> {i[2]} - |**{str(i[1])[6:]}|
<b>Текст обращения:</b>{i[3]}
<b>Время</B> {datetime.datetime.fromtimestamp(i[0])}""", reply_markup=keyboard_tc)

    # callback_data = f'question-{i[0]}')

    # InlineKeyboardButton('Ответить', callback_data=f'answer_off-{i[0]}')).add(
    # InlineKeyboardButton('Удалить', callback_data=f'delete_off-{i[0]}'))


async def contin(message, i, typ):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Продолжить', callback_data=f'ans-{i[1]}-{typ}')).add(
        InlineKeyboardButton('В архив', callback_data=f'archive-{i[1]}-{typ}'))

    if typ == "Обращение":
        typ = "️🛑🆘🆘🆘❌❌Обращение⛔️⛔️🛑🆘🆘🆘🛑"
    if i[6] != "Yes":
        await message.answer(f"""<b>{typ}️</b>
<b>Отправитель:</b> {i[2]} - |**{str(i[1])[6:]}|
<b>Предложение:</b> {i[3]}
""", reply_markup=keyboard_tc)


async def mailing(message, operator, typ):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'ans-{message.from_user.id}-{typ}')).add(
        InlineKeyboardButton('Удалить', callback_data=f'del-{message.from_user.id}-{typ}'))

    if typ == "Обращение":
        typ = "⛔️⛔️🛑🆘🆘🆘❌❌Обращение⛔️⛔️🛑🆘🆘🆘❌❌"
    await bot.send_message(operator,
f"""<b>{typ}</b>
<b>Отправитель:</b> {message.from_user.first_name} - |**{str(message.from_user.id)[6:]}|
<b>Текст обращения:</b>{message.text}
<b>Время</B> {message.date}""", reply_markup=keyboard_tc)


async def end(operator, name, ids, keyboard):
    await bot.send_message(operator,
                           f"{name} -"
                           f" |**{str(ids)[6:]}| завершил разговор",
                           reply_markup=keyboard)
