import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_connection_url():
    return make_url(os.getenv("CONNECTION_STRING"))


def create_engine_and_session():
    engine = create_engine(get_connection_url())
    Session = sessionmaker(engine)
    return engine, Session
