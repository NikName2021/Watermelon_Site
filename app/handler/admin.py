from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from additional import *
from connection import *
from additional.inline_keybords import *
from crud.userRequests import *
from crud.appealRequests import *
from crud.messageRequests import last_five_messages
# @dp.message_handler(Text(equals='Команды admin'))
from database.models import Appeals, Messages, User


async def commands_admin(message: types.Message):
    """
        Функция используется для вывода кнопок клавиатуры для команд admin
    """

    if message.from_user.id in main_user.admins:
        keyboard = await main_keyboard.admin_first()
        await message.answer("""Команды admin""", reply_markup=keyboard)
    else:
        await message.answer("Нет прав на данную команду")


"""   Управление операторами   """


# @dp.message_handler(Text(equals='Просмотр операторов'))
async def viewing_ad_and_op(message: types.Message):
    """
        Функция используется для вывода операторов
    """
    if message.from_user.id in main_user.admins:
        if main_user.operators:
            information_oper = '\n'.join([f"{i.telegram_id} - {i.name} (/del_{i.telegram_id})" for i in
                                          db.query(User).filter(User.role == ROLE_USERS['operator']).all()])
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
        await message.answer("Введите имя(никнейм) нового оператора")
        await machine.Opa.next()


# @dp.message_handler(state=machine.Opa.name)
async def add_operator_name(message: types.Message, state: FSMContext):
    """
        Функция используется для добавления нового оператора в бд
    """
    async with state.proxy() as data:
        ida = data["id"]
    user = User()
    user.name = message.text
    user.telegram_id = ida
    user.role = ROLE_USERS['operator']
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


# -------------------------------------------------------------------------------------------
"""Управление обращениями"""


# @dp.message_handler(Text(equals='Доступные обращения'))
async def free_appeals(message: types.Message):
    """
        Функция используется для различных выводов доступных обращений для ответа
    """
    if message.from_user.id in main_user.admins:
        app = db.query(Appeals).where(Appeals.status == 0, Appeals.operator_id == None).all()
        if not app:
            await message.answer("Ничего не найдено")
            return
        for i in app:
            await function.send_add(message, i)
    else:
        await message.answer("Нет прав на данную команду")


# @dp.callback_query_handler(main_filters.Dele())
async def del_appeal(call: types.CallbackQuery):
    """
        Функция удаления обращения из бд
    """

    ida = call.data.split("-")
    app = await get_appeal(ida[1])
    if not app.status and not app.operator_id:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await set_status(app, STATUS['delete'])
        await call.message.answer("Обращение удалено")
    elif app.status:
        await call.message.answer(f"Данного обращения уже не существует")
    else:
        await call.message.answer(f"У этого обращения уже есть оператор")


# @dp.callback_query_handler(main_filters.SendTo())
async def send_to(call: types.CallbackQuery, state: FSMContext):
    """
        Функция входа в машину ожидания сообщений для оператора
    """
    current_state = await state.get_state()
    if current_state:
        await call.message.answer("Вы находитесь в диалоге!!")
        return
    ida = call.data.split("-")
    operators = db.query(User).filter(User.role == ROLE_USERS['operator']).all()
    await call.message.answer("Выберете оператора для данного обращения:",
                              reply_markup=await create_all_operator_kb(operators, 'sendNewTo', ida[1]))


# @dp.callback_query_handler(main_filters.SendToOperator())
async def send_to_operator(call: types.CallbackQuery):

    ida = call.data.split("-")
    operator = await get_user(ida[1])
    appeal: Appeals = await get_appeal(ida[2])

    appeal.operator_id = operator.id
    db.commit()
    last_message = db.query(Messages).filter(Messages.appeal_id == int(ida[2])).all()[-1]
    try:
        await function.mailing_operator(operator.telegram_id, appeal, last_message.text)
    except Exception:
        pass
    await call.message.answer(f"Обращение перенаправленно на оператора <b>{operator.name}</b>")


# @dp.message_handler(Text(equals='Статус обращения'))
async def info_appeal(message: types.Message):

    if message.from_user.id in main_user.admins:
        await machine.InfoAppeal.id.set()
        await message.answer("Введите id обращения")
    else:
        await message.answer("Нет прав на данную команду")


# @dp.message_handler(state=machine.InfoAppeal.id)
async def info_appeal_id(message: types.Message, state: FSMContext):
    """
        Функция используется для ввода id обращения
    """
    if not message.text.isdigit():
        await message.answer("В ID содержатся буквы, попробуй снова")
        await asyncio.sleep(1)
    else:
        appeal = await get_appeal(message.text)
        if not appeal:
            await message.answer("Обращения с таким ID не существует")
        else:
            await message.answer(await function.information_for_admin(appeal),
                                 reply_markup=await about_appeal_kb(appeal.id))
        await state.finish()


# dp.register_callback_query_handler(check_messages, main_filters.CheckMessages())
async def check_messages(call: types.CallbackQuery):

    ida = call.data.split("-")
    messages = await last_five_messages(ida[1])
    for message in messages:
        type_message = '<b>Клиент</b>'
        if message.operator_type:
            type_message = '<b>Оператор</b>'
        await call.message.answer(f"""{type_message}
<b>Текст:</b> {message.text}

<b>Время:</b> {message.created_date.strftime("%d.%m.%Y %H-%M")}""")


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(viewing_ad_and_op, Text(equals='Просмотр операторов'))
    dp.register_message_handler(commands_admin, Text(equals='Команды admin'))
    dp.register_message_handler(add_operator, Text(equals='Добавить оператора'))
    dp.register_message_handler(add_operator_id, state=machine.Opa.id)
    dp.register_message_handler(add_operator_name, state=machine.Opa.name)
    dp.register_message_handler(del_operator, main_filters.Load())
    # ---------------------------------
    dp.register_message_handler(free_appeals, commands="appels_all")
    dp.register_message_handler(free_appeals, Text(equals='Доступные обращения'))
    dp.register_callback_query_handler(del_appeal, main_filters.Dele())
    dp.register_callback_query_handler(send_to, main_filters.SendTo())
    dp.register_callback_query_handler(send_to_operator, main_filters.SendToOperator())

    dp.register_message_handler(info_appeal, Text(equals='Статус обращения'))
    dp.register_message_handler(info_appeal_id, state=machine.InfoAppeal.id)
    dp.register_callback_query_handler(check_messages, main_filters.CheckMessages())
