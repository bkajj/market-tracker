from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@127.0.0.1:5433/market-db")
Session = sessionmaker(engine)
