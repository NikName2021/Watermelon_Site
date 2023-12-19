import os
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

DeclBase = declarative_base()


def run_migrate():
    load_dotenv()
    db_path = URL.create(
        drivername="postgresql",
        username=os.getenv("POSTGRES_USER"),
        host="postgres",
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DATABASE"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    engine = create_engine(db_path)
    DeclBase.metadata.create_all(engine)
