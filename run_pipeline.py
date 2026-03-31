from postgres.db import create_engine_and_session
from postgres.db_init import init_db
from postgres.load_data import load_to_db
from sqlalchemy.exc import OperationalError
from requests.exceptions import RequestException
from json import JSONDecodeError
from fetch_data import fetch_data_from_api, FetchAPIException
import logging
import datetime as dt

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        handlers=[logging.FileHandler('pipeline.log'), logging.StreamHandler()],
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S')
    
    try:
        logger.info("Starting pipeline...")
        engine, Session = create_engine_and_session()

        logger.info("Initializing database")
        init_db(engine)

        logger.info("Fetching data from API")
        first_available_day = dt.date.today() - dt.timedelta(days=4)
        raw_data = fetch_data_from_api('AAPL', 'minute', str(first_available_day), str(first_available_day))

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
    except Exception as e:
        logger.error(e, exc_info=True)

