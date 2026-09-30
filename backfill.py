from market_tracker.db.engine import create_engine_and_session
from market_tracker.fetch import fetch_to_file
from market_tracker.load import load_to_db
from market_tracker.config import BASE_DIR
import exchange_calendars as xcals
import pandas as pd
import datetime as dt
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)   

def find_missing_data(tickers, interval, engine, Session):
    max_history_days = 31
    api_delay_days = 4
    
    if interval == 'minute':
        expected_records_per_day = 390 # sometimes is 391
    elif interval == 'hour':
        expected_records_per_day = 7 # sometimes is 8
        
    df = pd.read_sql(text('SELECT id, ticker, timestamp FROM intraday_prices ORDER BY ticker, timestamp'), engine)
    max_date = dt.date.today() - dt.timedelta(days=max_history_days)
    
    # get market session dates and convert them to proper format
    xcal = xcals.get_calendar('XNYS') # TODO: get calendar from ticker name
    sessions = xcal.sessions_in_range(max_date, dt.date.today() - dt.timedelta(days=api_delay_days))
    session_dates = [s.date() for s in sessions]
    
    # get days from database, convert them to match sessions format
    df['timestamp'] = df['timestamp'].dt.date
    df = df[df['timestamp'] >= max_date]
    counts = df.groupby(['ticker', 'timestamp']).count()
    incomplete_days = counts[counts['id'] < expected_records_per_day] # if only part of the day has data
    
    for ticker in tickers:
        diff = set(session_dates) - set(df[df['ticker'] == ticker]['timestamp'])
        
        if not incomplete_days.empty and ticker in incomplete_days.index.get_level_values('ticker'):
            diff |= set(incomplete_days.loc[ticker].index) # theoretically should't even happen
            
        logger.info(f'Getting missing {len(diff)} days for {ticker}')
            
        for day in sorted(diff):
            filename = fetch_to_file(ticker, interval, day, BASE_DIR / 'data')
            load_to_db(filename, interval, Session)
        
        
if __name__ == "__main__":
    e, s = create_engine_and_session()
    find_missing_data(['META'], 'minute', e, s)