from aiogram.dispatcher.filters.state import StatesGroup, State


class Appeal(StatesGroup):
    """
        Класс машины состояний,
        который ожидает сообщение пользователя
    """
    text = State()


class Question(StatesGroup):
    """
        Класс машины состояний,
        который вопрос пользователя
    """
    text = State()


class Offers(StatesGroup):
    """
        Класс машины состояний,
        который вопрос пользователя
    """
    text = State()


class AnswerOffers(StatesGroup):
    """
        Класс машины состояний,
        который вопрос пользователя
    """
    text = State()


class Opearator(StatesGroup):
    """
        Класс машины состояний,
        который ожидает сообщение оператора
    """
    mess = State()


class MainOffer(StatesGroup):
    """
        Класс машины состояний,
        который ожидает сообщение оператора
    """
    mess = State()


class Add(StatesGroup):
    """
        Класс машины состояний,
        который ожидает id и имя нового админа
    """
    id = State()
    name = State()


class Opa(StatesGroup):
    """
        Класс машины состояний,
        который ожидает id и имя нового оператора
        """
    id = State()
    password = State()
    name = State()
