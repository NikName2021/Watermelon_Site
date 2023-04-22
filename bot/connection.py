from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from database.__all_models import *
from database.db_session import create_session
from helpers import role_user

load_dotenv()


async def update_operators():
    """Функция обновления данных из бд
    после добавления нового админа или оператора"""

    global admins
    global operators
    operators = [i[0] for i in db.query(User.telegram_id).filter(User.role == role_user.ROLE_USERS['operator']).all()]
    admins = [i[0] for i in db.query(User.telegram_id).filter(User.role == role_user.ROLE_USERS['admin']).all()]


BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = create_session()
operators = [i[0] for i in db.query(User.telegram_id).filter(User.role == role_user.ROLE_USERS['operator']).all()]
admins = [i[0] for i in db.query(User.telegram_id).filter(User.role == role_user.ROLE_USERS['admin']).all()]
