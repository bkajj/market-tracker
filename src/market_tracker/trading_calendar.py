import exchange_calendars
import datetime

def is_trading_day(date: datetime.date, market: str = "XNYS") -> bool:
    return exchange_calendars.get_calendar(market).is_session(date)