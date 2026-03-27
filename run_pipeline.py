from postgres.db import create_engine_and_session
from postgres.db_init import init_db
from postgres.load_data import load_to_db
from fetch_data import fetch_data_from_api

if __name__ == "__main__":
    engine, Session = create_engine_and_session()
    init_db(engine)
    raw_data = fetch_data_from_api('AAPL', 'hour', '2024-01-01', '2022-01-31')
    load_to_db(raw_data, Session)
