import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from config import BASE_DIR
import logging
logger = logging.getLogger(__name__)


load_dotenv()

class FetchAPIException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

def fetch_data_from_api(symbols, interval, date_from, date_to):
    params = {
        'api_token': os.getenv('STOCKDATA_API_TOKEN'),
        'symbols': symbols,
        'interval': interval,
        'date_from': date_from, 
        'date_to': date_to
    }
    filtered_params = {k: v for k, v in params.items() if v is not None and v != ''}

    url = 'https://api.stockdata.org/v1/data/intraday'
    r = requests.get(url, params=filtered_params)
    json_data = r.json()

    if "error" in json_data:
        raise FetchAPIException(json_data['error']['code'], json_data['error']['message'])

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = BASE_DIR / 'data' / f'data_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)
        logger.info(f'Saved to file {f'data/data_{timestamp}.json'}')

    return json_data

if __name__ == "__main__":
    fetch_data_from_api('AAPL', 'hour', '2022-03-11', '2022-03-11')