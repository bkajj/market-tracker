from .db_models import Base
from .db import create_engine_and_session

def init_db(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    e, _ = create_engine_and_session()
    init_db(e)