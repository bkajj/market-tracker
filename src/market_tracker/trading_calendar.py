from datetime import date, datetime, timedelta

import exchange_calendars


def is_trading_day(day: date, market: str = "XNYS") -> bool:
    return exchange_calendars.get_calendar(market).is_session(day)


def target_day(logical_date: datetime, delay_days: int) -> date:
    return logical_date.date() - timedelta(days=delay_days)
