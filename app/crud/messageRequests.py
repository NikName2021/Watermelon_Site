from database import *
from connection import db
from database.models import Messages


async def message_create(appeal_id, text, operator_type):
    db.add(Messages(appeal_id=int(appeal_id), operator_type=operator_type, text=text))
    db.commit()


async def first_message(appeal_id):
    return db.query(Messages).where(Messages.appeal_id == int(appeal_id)).first()


async def last_five_messages(appeal_id):
    return db.query(Messages).where(Messages.appeal_id == int(appeal_id)).order_by(Messages.id).all()[-5:]
