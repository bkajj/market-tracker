from config import BASE_DIR
from .db import Session
from .db_models import IntradayPrice
import json

records = []
with open(BASE_DIR/'data/data.json') as f:
    raw = json.load(f)
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