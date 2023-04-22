from datetime import datetime, date
import re
from random import choice

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import *
from bot.connection import *


async def get_phrase(user_tg):
    """Функция формирования фразы дня"""
    checks = db.query(UserPhrases).filter(UserPhrases.user_id == user_tg).all()
    variants = db.query(Phrase).all()
    if not checks:
        phrase = choice(variants)
        db.add(UserPhrases(user_id=user_tg, phrase_id=phrase.id))
        db.commit()
        return phrase.text

    else:
        # checks = checks[0]
        newdate1 = checks[-1].created_date.strftime("%Y-%m-%d")
        if newdate1 == str(date.today()):
            return db.query(Phrase).get(checks[-1].phrase_id).text
        else:
            if len(checks) == 7:
                for i in checks:
                    db.delete(i)
                db.commit()
            phrase = choice(variants)
            while phrase.id in [i.phrase_id for i in checks]:
                phrase = choice(EVERYDAY)
            db.add(UserPhrases(user_id=user_tg, phrase_id=phrase.id))
            db.commit()
            return phrase.text


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


async def send_add(message, i):
    typ = HElP_FOR_KEYBOARD[i.type]
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'ans-{i.id}-{typ}')).add(
        InlineKeyboardButton('Удалить', callback_data=f'del-{i.id}-{typ}'))
    mes = db.query(Messages).where(Messages.appeal_id == i.id).first()

    await message.answer(f"""<b>{DETERMINATION[i.type]}</b>
<b>Отправитель:</b> {i.client_name} - |**{str(i.client_id)[6:]}|
<b>Текст обращения:</b>{mes.text}
<b>Время</B> {i.created_date.strftime("%Y-%m-%d")}""", reply_markup=keyboard_tc)


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
