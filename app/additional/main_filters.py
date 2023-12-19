from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from connection import main_user


class Load(BoundFilter):
    """
        Класс - фильтр, обнаруживающий команду для удаления оператора
    """
    async def check(self, message: types.Message):
        tx = message.text.split('_')
        if tx[0] == "/del" and int(tx[1]) in main_user.operators:
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


