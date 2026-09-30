from market_tracker.db.engine import create_engine_and_session
from market_tracker.db.schema import init_db
from market_tracker.load import load_to_db
from market_tracker.config import BASE_DIR
from sqlalchemy.exc import OperationalError
from requests.exceptions import RequestException
from json import JSONDecodeError
from market_tracker.fetch import fetch_to_file, FetchAPIException
import logging
import datetime as dt
import yaml
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    try:
        logger.info("Starting pipeline...")
        engine, Session = create_engine_and_session()

        logger.info("Initializing database")
        init_db(engine)

        logger.info("Parsing YAML file")
        with open('request_data.yaml') as f:
            request_data = yaml.safe_load(f)
            interval = request_data['interval']

            if request_data['date']['mode'] == 'latest':
                #TODO: it should check for nearset workday
                date_from = date_to = dt.date.today() - dt.timedelta(days=4)
            elif request_data['date']['mode'] == 'range':
                date_from = request_data['date']['from'] 
                date_to = request_data['date']['to']

            date_range = date_to - date_from
            for ticker in request_data['tickers']:
                for i in range(date_range.days + 1):
                    day = date_from + dt.timedelta(i)
                    if day.weekday() >= 5: # saturdays and sundays
                        continue
                    logger.info(f"Fetching data from API for ticker {ticker} at {day}")
                    filepath = fetch_to_file(ticker, interval, day, BASE_DIR / 'data')
                    logger.info("Saving data to database")
                    load_to_db(filepath, interval, Session)

        logger.info("Pipeline finished successfully:)")

    except Exception:
        logger.exception("Pipeline failed")
        raise

