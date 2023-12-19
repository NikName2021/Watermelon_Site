from aiogram.dispatcher.filters.state import StatesGroup, State


class Question(StatesGroup):
    """
        Класс машины состояний,
        который вопрос пользователя
    """
    text = State()


class AnswerOffers(StatesGroup):

    text = State()


class MainOffer(StatesGroup):
    """
        Класс машины состояний,
        который ожидает сообщение оператора
    """
    mess = State()


class Opa(StatesGroup):
    """
        Класс машины состояний,
        который ожидает id и имя нового оператора
        """
    id = State()
    name = State()
