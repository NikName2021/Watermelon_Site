from config import STATUS
from database import *
from connection import db
from database.models import Appeals


async def get_appeal(id):
    return db.query(Appeals).get(int(id))


async def get_appeals_user(user_id):
    return db.query(Appeals).where(Appeals.operator_id == user_id, Appeals.status == STATUS['work']).all()


async def set_status(appeal, status):
    appeal.status = int(status)
    db.commit()
