from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_engine_and_session():
    engine = create_engine("postgresql+psycopg2://admin:admin@127.0.0.1:5433/market-db")
    Session = sessionmaker(engine)
    return engine, Session