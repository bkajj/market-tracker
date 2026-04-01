from postgres.db import create_engine_and_session
from postgres.db_init import init_db
from postgres.load_data import load_to_db
from sqlalchemy.exc import OperationalError
from requests.exceptions import RequestException
from json import JSONDecodeError
from fetch_data import fetch_data_from_api, FetchAPIException
import logging
import datetime as dt
import yaml
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        handlers=[logging.FileHandler('pipeline.log'), logging.StreamHandler()],
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S')
    
    try:
        raw_data = []

        logger.info("Starting pipeline...")
        engine, Session = create_engine_and_session()

        logger.info("Initializing database")
        init_db(engine)

        logger.info("Parsing YAML file")
        with open('request_data.yaml') as f:
            request_data = yaml.safe_load(f)
            interval = request_data['interval']

            if request_data['date']['mode'] == 'latest':
                date_from = date_to = str(dt.date.today() - dt.timedelta(days=4))
            elif request_data['date']['mode'] == 'range':
                date_from = request_data['date']['from'] 
                date_to = request_data['date']['to']

            for ticker in request_data['tickers']:
                logger.info(f"Fetching data from API for ticker {ticker}")
                raw_data.append(fetch_data_from_api(ticker, interval, date_from, date_to))

        logger.info("Saving data to database")
        load_to_db(raw_data, Session)

        logger.info("Pipeline finished successfully:)")

    except OperationalError:
        logger.error("Couldn't connect to database", exc_info=True)
    except RequestException:
        logger.error("Couldn't connect to API", exc_info=True)
    except JSONDecodeError as e:
        logger.error(f"Couldn't decode JSON file {e.doc}", exc_info=True)
    except FetchAPIException as e:
        logger.error(f"API Error {e.code}: {str(e)}", exc_info=True)
    except yaml.YAMLError:
        logger.error(f"YAML parsing error", exc_info=True)
    except KeyError as e:
        logger.error(f'Invalid index {str(e)}', exc_info=True)
    except Exception as e:
        logger.error(e, exc_info=True)

