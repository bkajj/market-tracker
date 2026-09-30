from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

def create_engine_and_session():
    engine = create_engine(os.getenv("CONNECTION_STRING"))
    Session = sessionmaker(engine)
    return engine, Session