import requests
import json
import os
from dotenv import load_dotenv
import logging
import datetime
from pathlib import Path
logger = logging.getLogger(__name__)

load_dotenv()

class FetchAPIException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

def fetch_to_file(ticker: str, interval: str, date: datetime.date, data_path: Path | str):
    token = os.getenv('STOCKDATA_API_TOKEN')
    if not token:
        raise RuntimeError("STOCKDATA_API_TOKEN is not set")
    
    params = {
        'api_token': token,
        'symbols': ticker,
        'interval': interval,
        'date_from': date, # for some weird reason providing 'date' wont work
        'date_to': date, # need to provide range from ... to
    }

    url = 'https://api.stockdata.org/v1/data/intraday'
    r = requests.get(url, params=params, timeout=30)
    try:
        json_data = r.json()
    except requests.exceptions.JSONDecodeError:
        r.raise_for_status()
        raise

    if "error" in json_data:
        raise FetchAPIException(json_data['error']['code'], json_data['error']['message'])
    r.raise_for_status()
    
    filename = Path(data_path) / 'raw' / 'intraday' / f'interval={interval}' / f'ticker={ticker}' / f'date={date}.json'
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)
        logger.info(f'Saved to file {filename}')
    
    return filename

if __name__ == "__main__":
    fetch_to_file('AAPL', 'hour', '2026-09-24', 'data')