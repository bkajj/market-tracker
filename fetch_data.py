import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

params = {
    'api_token': os.getenv('STOCKDATA_API_TOKEN'),
    'symbols': 'AAPL',
    'interval': 'hour',             # minute, hour
    'sort': '',                     # asc, dsc
    'date_from': '2026-03-18',                # Y-m-d | Y-m | Y
    'date_to': '2026-03-18',                  # Y-m-d | Y-m | Y
    'date': '',           # Y-m-d
    'extended_hours': '',
    'key_by_date': '',
    'key_by_ticker': '',
    'format': ''                    # csv, json
}

filtered_params = {k: v for k, v in params.items() if v is not None and v != ''}


url = f'https://api.stockdata.org/v1/data/intraday'
r = requests.get(url, params=filtered_params)

with open('data.json', 'w') as f:
    json.dump(r.json(), f, indent=2)
    print("Saved to file data.json")