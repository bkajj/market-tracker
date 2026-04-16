from config import BASE_DIR
from .db_models import IntradayPrice
from .db import create_engine_and_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, text
import json
import logging
import pandas as pd
logger = logging.getLogger(__name__)

# def find_missing_data_in_db(tickers, engine):
#     df = pd.read_sql(text('SELECT ticker, timestamp FROM intraday_prices ORDER BY ticker, timestamp'), engine)
#     #df = df.groupby(['ticker', df['timestamp'].dt.date]).count()
#     print(df)
    
def load_from_file(filename=BASE_DIR/'data/data.json'):
    with open(filename) as f:
        return json.load(f)

def load_to_db(raw, interval, Session):
    records = []

    for ticker_data in raw:
        meta = ticker_data['meta']
        data = ticker_data['data']
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
        logger.warning('No data fetched')
        return

    with Session() as session:
        count_records_stmt = select(func.count("*")).select_from(IntradayPrice)
        count_before = session.execute(count_records_stmt).scalar()

        insert_stmt = insert(IntradayPrice).values(records)
        insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['ticker', 'timestamp', 'interval'])
        session.execute(insert_stmt)
        session.commit()

        count_after = session.execute(count_records_stmt).scalar()

        logger.info(f"{count_after-count_before} of {len(records)} rows affected")

if __name__ == "__main__":
    e, s = create_engine_and_session()
    
    # find_missing_data_in_db('AAPL', e)
    
    d = []
    d.append(load_from_file())
    load_to_db(d, s)