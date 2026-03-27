from config import BASE_DIR
from .db_models import IntradayPrice
from .db import create_engine_and_session
import json

def load_from_file(filename=BASE_DIR/'data/data.json'):
    with open(filename) as f:
        return json.load(f)

def load_to_db(raw, Session):
    records = []        
    meta = raw['meta']
    data = raw['data']
    for d in data:
        records.append(
            IntradayPrice(
                ticker=d['ticker'],
                timestamp=d['date'],
                open=d['data']['open'],
                high=d['data']['high'],
                low=d['data']['low'],
                close=d['data']['close'],
                volume=d['data']['volume'],
                ext_hours=d['data']['is_extended_hours'],
        ))

    with Session() as session:
        session.add_all(records)
        session.commit()

if __name__ == "__main__":
    _, s = create_engine_and_session()
    d = load_from_file()
    load_to_db(d, s)