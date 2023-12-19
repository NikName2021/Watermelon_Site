import datetime
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .dec_db import DeclBase


class Phrase(DeclBase):
    __tablename__ = 'phrases'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    phrase_user = relationship("UserPhrases")


class UserPhrases(DeclBase):
    __tablename__ = 'user_phrases'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    phrase_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  ForeignKey('phrases.id'))