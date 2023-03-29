import sqlite3

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
con = sqlite3.connect('base.db')
cur = con.cursor()
operators = [i[0] for i in cur.execute(f"SELECT * FROM user").fetchall() if "operator" in i[2].split()]
admins = [i[0] for i in cur.execute(f"SELECT * FROM user").fetchall() if "admin" in i[2].split()]