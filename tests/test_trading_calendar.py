from datetime import UTC, date, datetime

import pytest

from market_tracker.trading_calendar import is_trading_day, target_day


@pytest.mark.parametrize(
    "day, expected",
    [
        pytest.param(date(2026, 9, 21), True, id="regular_weekday"),
        pytest.param(date(2026, 9, 26), False, id="saturday"),
        pytest.param(date(2026, 12, 25), False, id="christmas"),
        pytest.param(date(2026, 4, 3), False, id="good_friday"),
        pytest.param(date(2026, 9, 7), False, id="labor_day"),
        pytest.param(date(2026, 7, 3), False, id="independence_day_observed"),
        pytest.param(date(2026, 11, 27), True, id="day_after_thanksgiving"),
    ],
)
def test_is_trading_day(day, expected):
    assert is_trading_day(day) == expected


@pytest.mark.parametrize(
    "logical_date, delay_days, expected",
    [
        pytest.param(
            datetime(2026, 9, 29, 22, tzinfo=UTC),
            4,
            date(2026, 9, 25),
            id="within_months",
        ),
        pytest.param(
            datetime(2026, 10, 2, 22, tzinfo=UTC),
            4,
            date(2026, 9, 28),
            id="crosses_month_boundary",
        ),
        pytest.param(
            datetime(2026, 10, 2, 22, tzinfo=UTC), 0, date(2026, 10, 2), id="no_delay"
        ),
    ],
)
def test_target_day(logical_date, delay_days, expected):
    assert target_day(logical_date, delay_days) == expected
