import datetime
import os
import sqlalchemy
from sqlalchemy import ForeignKey, create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.engine import URL
from dotenv import load_dotenv

DeclBase = declarative_base()


class User(DeclBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(sqlalchemy.BigInteger, unique=True)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    role = Column(Integer)
    created_date = Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    appels = relationship('Appeals')


class Appeals(DeclBase):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(sqlalchemy.BigInteger)
    client_name = Column(String, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(Integer, nullable=True)
    status = Column(Integer)
    user_status = Column(sqlalchemy.Boolean, default=False)
    created_date = Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    messages = relationship("Messages")


class Messages(DeclBase):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    appeal_id = Column(Integer, ForeignKey("appeals.id"))
    operator_type = Column(sqlalchemy.Boolean)
    text = Column(String, nullable=True)
    created_date = Column(sqlalchemy.DateTime, default=datetime.datetime.now)


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
