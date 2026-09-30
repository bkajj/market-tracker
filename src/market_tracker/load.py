from market_tracker.db.models import IntradayPrice
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)   

def load_to_db(path: Path | str, interval: str, Session: Session):
    records = []

    with open(path, 'r') as f:
        raw = json.load(f)

    meta = raw['meta']
    data = raw['data']
    for d in data:
        records.append({
            'ticker': d['ticker'],
            'timestamp': d['date'],
            'interval': interval,
            'open': d['data']['open'],
            'high': d['data']['high'],
            'low': d['data']['low'],
            'close': d['data']['close'],
            'volume': d['data']['volume'],
            'ext_hours': d['data']['is_extended_hours'],
        })

    if len(records) == 0:
        raise RuntimeError("No data fetched")

    with Session() as session:
        insert_stmt = insert(IntradayPrice).values(records)
        insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['ticker', 'timestamp', 'interval'])
        result = session.execute(insert_stmt)
        session.commit()

        logger.info(f"{result.rowcount} of {len(records)} rows affected")