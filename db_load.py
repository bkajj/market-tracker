from sqlalchemy import create_engine
from db_models import Base

engine = create_engine("postgresql+psycopg2://admin:admin@127.0.0.1:5433/market-db")
Base.metadata.create_all(engine)