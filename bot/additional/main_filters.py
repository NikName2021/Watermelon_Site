from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.connection import operators


class Load(BoundFilter):
    """
        Класс - фильтр, обнаруживающий команду для удаления оператора
    """
    async def check(self, message: types.Message):
        tx = message.text.split('_')
        if tx[0] == "/del" and int(tx[1]) in operators:
            return True

        return False


class Ans(BoundFilter):
    """
        Класс - фильтр, позволяющий отследить
        нажатие кнопки "Ответить" для оператора
    """
    async def check(self, call: types.CallbackQuery):
        tx = call.data.split("-")
        if tx[0] == "ans":
            return True
        return False


class Dele(BoundFilter):
    """
        Класс - фильтр, позволяющий отследить
        нажатие кнопки "Удалить обращение" для оператора
    """
    async def check(self, call: types.CallbackQuery):
        tx = call.data.split("-")
        if tx[0] == "del":
            return True
        return False


class Archive(BoundFilter):
    """
        Класс - фильтр, позволяющий отследить
        нажатие кнопки "Удалить обращение" для оператора
    """
    async def check(self, call: types.CallbackQuery):
        tx = call.data.split("-")
        if tx[0] == "archive":
            return True
        return False


class Main(BoundFilter):
    """
        Класс - фильтр, позволяющий отследить
        нажатие кнопки "Удалить обращение" для оператора
    """
    async def check(self, call: types.CallbackQuery):
        tx = call.data.split("-")
        if tx[0] == "main":
            return True
        return False


# class Off_del(BoundFilter):
#     """
#         Класс - фильтр, позволяющий отследить
#         нажатие кнопки "Ответить" для оператора
#     """
#     async def check(self, call: types.CallbackQuery):
#         tx = call.data.split("-")
#         if tx[0] == "delete_off" and tx[1].isdigit():
#             return True
#         return False
#
#
# class Off_main(BoundFilter):
#     """
#         Класс - фильтр, позволяющий отследить
#         нажатие кнопки "Ответить" для оператора
#     """
#     async def check(self, call: types.CallbackQuery):
#         tx = call.data.split("-")
#         if tx[0] == "answer_off" and tx[1].isdigit():
#             return True
#         return False
#
#
# class Que(BoundFilter):
#     """
#         Класс - фильтр, позволяющий отследить
#         нажатие кнопки "Ответить" для оператора
#     """
#     async def check(self, call: types.CallbackQuery):
#         tx = call.data.split("-")
#         if tx[0] == "question" and "_" in tx[1]:
#             return True
#         return False
#

