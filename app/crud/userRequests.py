from database.models import User
from connection import db


async def get_user(user_id) -> User:
    return db.query(User).get(int(user_id))


async def get_user_telegram(telegram_id):
    return db.query(User).filter(User.telegram_id == int(telegram_id)).first()
