from connection import *
from handler import *
from additional import *
from aiogram import executor, types


async def on_startup(dp):
    dp.filters_factory.bind(main_filters.Load)
    dp.filters_factory.bind(main_filters.Ans)
    dp.filters_factory.bind(main_filters.Dele)
    dp.filters_factory.bind(main_filters.Archive)
    dp.filters_factory.bind(main_filters.Main)
    # dp.filters_factory.bind(main_filters.Off_del)
    # dp.filters_factory.bind(main_filters.Que)


add.register_handler_add(dp)
user.register_handler_user(dp)
# operator.register_handler_operator(dp)


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)