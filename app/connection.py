import os
import asyncio
import nest_asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.User import User
from database.db_session import create_session
from database import run_migrate, run_seeder
from dotenv import load_dotenv
from config import ROLE_USERS

load_dotenv()


class ListMainPeople:
    def __init__(self):
        self.operators = []
        self.admins = []
        self.loop = asyncio.get_event_loop()
        self.ping()

    async def update_operators(self):
        """Функция обновления данных из бд
        после добавления нового админа или оператора"""

        self.operators = [i[0] for i in
                          db.query(User.telegram_id).filter(User.role == ROLE_USERS['operator']).all()]
        self.admins = [i[0] for i in
                       db.query(User.telegram_id).filter(User.role == ROLE_USERS['admin']).all()]

    def ping(self):
        nest_asyncio.apply()
        return self.loop.run_until_complete(self._ping())

    async def _ping(self):
        await self.update_operators()


BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
run_migrate()
# run_seeder()
db = create_session()
main_user = ListMainPeople()
