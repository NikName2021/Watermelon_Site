from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def sorting_mailing(appeal_id, typ):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'ans-{appeal_id}-{typ}')).add(
        InlineKeyboardButton('Отправить оператору', callback_data=f'sendBy-{appeal_id}-{typ}')).add(
        InlineKeyboardButton('Удалить', callback_data=f'del-{appeal_id}-{typ}'))

    return keyboard


async def keyboard_to_operator_send(app_id, typ):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'ans-{app_id}-{typ}'))

    return keyboard_tc


async def keyboard_to_client_send(app_id):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Ответить', callback_data=f'main-{app_id}'))

    return keyboard_tc


async def continue_appeal_kb(appeal_id, typ):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Продолжить', callback_data=f'ans-{appeal_id}-{typ}')).add(
        InlineKeyboardButton('В архив', callback_data=f'archive-{appeal_id}-{typ}'))
    return keyboard_tc


async def create_all_operator_kb(operators, prefix, id_appeal):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for operator in operators:
        keyboard.add(InlineKeyboardButton(operator.name, callback_data=f'{prefix}-{operator.id}-{id_appeal}'))
    return keyboard


async def about_appeal_kb(appeal_id):
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Последние 5 сообщений', callback_data=f'messages-{appeal_id}')).add(
        InlineKeyboardButton('Изменить оператора', callback_data=f'sendBy-{appeal_id}'))
    return keyboard_tc


async def SOS_kb():
    keyboard_tc = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('SOS! Мне нужна срочная помощь', callback_data=f'help_keyboard'))
    return keyboard_tc
