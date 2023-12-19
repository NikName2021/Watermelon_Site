from aiogram import executor
from connection import *
from handler import *
from additional import *


async def on_startup(dp):
    dp.filters_factory.bind(main_filters.Load)
    dp.filters_factory.bind(main_filters.Ans)
    dp.filters_factory.bind(main_filters.Dele)
    dp.filters_factory.bind(main_filters.Archive)
    dp.filters_factory.bind(main_filters.Main)


async def on_shutdown():
    db.close()
    print('Соединение закрыто')

add.register_handler_add(dp)
user.register_handler_user(dp)
operator.register_handler_operator(dp)
admin.register_handler_admin(dp)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def if_the_text(msg: types.Message):
    """
        Функция ответа бота на неизвестную команду
    """
    az = await function.check_filter(msg)
    if az == 1:
        pass
    else:
        await msg.answer('Неизвестная для меня команда :(')
        print(msg.from_user)


def run_bot():
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    run_bot()
