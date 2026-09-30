from datetime import date, datetime, timedelta
from pathlib import Path
 
import pendulum
import yaml
from airflow.sdk import dag, task, task_group

API_DELAY_DAYS = 4

def _load_config() -> dict:
    config_path = Path(__file__).parent / 'pipeline_config.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)

CONFIG = _load_config()
TICKERS = CONFIG["tickers"]
INTERVAL = CONFIG["interval"]

def _target_day(logical_date: datetime) -> date:
    return logical_date.date() - timedelta(days=API_DELAY_DAYS)

@dag(
    dag_id="market_tracker",
    schedule="0 22 * * *",  # everyday at 22:00 UTC, check_trading_day skips closed days 
    start_date=pendulum.datetime(2026, 9, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["market-tracker"],
)
def market_tracker():

    @task.short_circuit
    def check_trading_day(logical_date=None) -> bool:
        from market_tracker.trading_calendar import is_trading_day

        day = _target_day(logical_date)
        print(f"Target day: {day}")
        return is_trading_day(day)

    @task
    def init_schema():
        from market_tracker.db.engine import create_engine_and_session
        from market_tracker.db.schema import init_db

        engine, _ = create_engine_and_session()
        init_db(engine)
        engine.dispose()

    @task
    def fetch(ticker: str, logical_date=None) -> str:
        import os
        from market_tracker.fetch import fetch_to_file

        path = fetch_to_file(
            ticker=ticker, 
            interval=INTERVAL, 
            date=_target_day(logical_date),
            data_path=os.environ["DATA_DIR"],
        )
        return str(path)

    @task
    def load(path: str):
        from market_tracker.db.engine import create_engine_and_session
        from market_tracker.load import load_to_db

        engine, Session = create_engine_and_session()
        load_to_db(
            path=path, 
            interval=INTERVAL, 
            Session=Session
        )
        engine.dispose()

    @task_group
    def process_ticker(ticker: str):
        path = fetch(ticker)
        load(path)

    check_trading_day() >> init_schema() >> process_ticker.expand(ticker=TICKERS)

market_tracker()