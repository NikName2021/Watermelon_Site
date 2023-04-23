import datetime
import os
import sqlalchemy
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.engine import URL
from dotenv import load_dotenv

DeclBase = declarative_base()


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


if __name__ == '__main__':
    load_dotenv()
    db_path = URL.create(
        drivername="postgresql",
        username=os.getenv("POSTGRES_USER"),
        host="localhost",
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DATABASE"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    engine = create_engine(db_path)
    DeclBase.metadata.create_all(engine)
