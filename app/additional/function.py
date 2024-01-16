import re
from datetime import date
from random import choice
from additional.inline_keybords import *
from config import *
from database.UserPhrase import UserPhrases, Phrase
from connection import *
from crud import *


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
                phrase = choice(variants)
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


async def information_appeal(appeal, text):
    return f"""<b>{DETERMINATION[appeal.type]}</b>
<b>ID обращения:</b> {appeal.id}
<b>Отправитель:</b> {appeal.client_name} - |**{str(appeal.client_id)[6:]}|
<b>Текст обращения:</b>{text}
<b>Время</B> {appeal.created_date.strftime("%d.%m.%Y %H-%M")}"""


async def send_add(message, appeal):
    typ = HElP_FOR_KEYBOARD[appeal.type]
    keyboard_tc = await sorting_mailing(appeal.id, typ)
    mes = await messageRequests.first_message(appeal.id)

    await message.answer(await information_appeal(appeal, mes.text), reply_markup=keyboard_tc)


async def continue_appeal(message, appeal):
    typ = HElP_FOR_KEYBOARD[appeal.type]
    mes = await messageRequests.first_message(appeal.id)
    await message.answer(await information_appeal(appeal, mes.text),
                         reply_markup=await continue_appeal_kb(appeal.id, typ))


async def mailing_for_sorting(message, admin, appeal):
    typ = HElP_FOR_KEYBOARD[appeal.type]
    await bot.send_message(admin, await information_appeal(appeal, message.text),
                           reply_markup=await sorting_mailing(appeal.id, typ))


async def mailing_operator(operator_id, appeal, text):
    typ = HElP_FOR_KEYBOARD[appeal.type]
    await bot.send_message(operator_id, await information_appeal(appeal, text),
                           reply_markup=await keyboard_to_operator_send(appeal.id, typ))


async def information_for_admin(appeal):
    if appeal.operator_id:
        operator = await userRequests.get_user(appeal.operator_id)
        operator_information = f"<b>Оператор:</b> {operator.name} || {operator.telegram_id}"
    else:
        operator_information = f"<b>Оператор:</b> Оператор не назначен"
    last_message = await messageRequests.first_message(appeal.id)
    return f"""{await information_appeal(appeal, last_message.text)}
    
{operator_information}
<b>Статус клиента:</b> {appeal.user_status}
<b>Статус обращения:</b> {STATUS_REVERSE[appeal.status]}"""


async def end(operator, name, ids, keyboard):
    await bot.send_message(operator,
                           f"{name} -"
                           f" |**{str(ids)[6:]}| завершил разговор",
                           reply_markup=keyboard)
