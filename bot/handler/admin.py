from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from werkzeug.security import generate_password_hash
from bot.additional import *
from bot.connection import *


# @dp.message_handler(Text(equals='Команды admin'))
async def commands_admin(message: types.Message):
    """
        Функция используется для вывода кнопок клавиатуры для команд admin
    """

    if message.from_user.id in main_user.admins:
        keyboard = await main_keyboard.admin_first()
        await message.answer("""Команды admin""", reply_markup=keyboard)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals='Просмотр операторов'))
async def viewing_ad_and_op(message: types.Message):
    """
        Функция используется для вывода операторов
    """
    if message.from_user.id in main_user.admins:
        if main_user.operators:
            information_oper = '\n'.join([f"{i.telegram_id} - {i.name} (/del_{i.telegram_id})" for i in
                    db.query(User).filter(User.role == role_user.ROLE_USERS['operator']).all()])
            await message.answer(f"""
<b>Операторы:</b>
{information_oper}""")
        else:
            await message.answer('Пока ни одного оператора не добавлено')
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(Text(equals='Добавить оператора'))
async def add_operator(message: types.Message):
    """
        Функция входа в машину ожиданий для добавления оператора
    """
    if message.from_user.id in main_user.admins:
        await machine.Opa.id.set()
        await message.answer("Введите id нового оператора")
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(state=machine.Opa.id)
async def add_operator_id(message: types.Message, state: FSMContext):
    """
        Функция используется для ввода id оператора
    """
    if not message.text.isdigit():
        await message.answer("В id содержатся буквы, попробуй снова")
        await asyncio.sleep(1)
    elif int(message.text) in main_user.operators + main_user.admins:
        await message.answer("Такой оператор существует, введи другой id")
        await asyncio.sleep(1)
    else:
        async with state.proxy() as data:
            data["id"] = message.text
        await message.answer("Введите пароль для сайта нового оператора")
        await machine.Opa.next()


# @dp.message_handler(state=machine.Opa.password)
async def add_operator_password(message: types.Message, state: FSMContext):
    """
        Функция используется для ввода password оператора
    """
    if len(message.text) > 8:
        async with state.proxy() as data:
            data["password"] = generate_password_hash(message.text)
        await message.answer("Введите имя(никнейм) нового оператора")
        await machine.Opa.next()
    else:
        await message.answer("Пароль должен быть длиннее 8 символов, попробуй снова")
        await asyncio.sleep(1)


# @dp.message_handler(state=machine.Opa.name)
async def add_operator_name(message: types.Message, state: FSMContext):
    """
        Функция используется для добавления нового оператора в бд
    """
    async with state.proxy() as data:
        ida = data["id"]
        password = data['password']
    user = User()
    user.name = message.text
    user.telegram_id = ida
    user.role = role_user.ROLE_USERS['operator']
    user.hashed_password = password
    db.add(user)
    db.commit()
    main_user.ping()
    await message.answer(f"Оператор {ida}({message.text}) успешно добавлен.")
    await state.finish()


# @dp.message_handler(main_filters.Load())
async def del_operator(message: types.Message):
    """
        Функция используется для удаления оператора
    """
    ids = message.text.split("_")[1]
    operator = db.query(User).where(User.telegram_id == ids).first()
    db.delete(operator)
    db.commit()
    main_user.ping()
    await message.answer(f"Оператор {ids} удален")


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(viewing_ad_and_op, Text(equals='Просмотр операторов'))
    dp.register_message_handler(commands_admin, Text(equals='Команды admin'))
    dp.register_message_handler(add_operator, Text(equals='Добавить оператора'))
    dp.register_message_handler(add_operator_id, state=machine.Opa.id)
    dp.register_message_handler(add_operator_password, state=machine.Opa.password)
    dp.register_message_handler(add_operator_name, state=machine.Opa.name)
    dp.register_message_handler(del_operator, main_filters.Load())
