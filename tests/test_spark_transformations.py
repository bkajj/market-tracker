from datetime import date, datetime

import pytest

from market_tracker.spark.transformations import add_daily_metrics, aggregate_daily

INTRADAY_COLUMNS = ["ticker", "timestamp", "open", "high", "low", "close", "volume", "ext_hours"]
DAILY_COLUMNS = ["ticker", "date", "open", "high", "low", "close", "volume"]


def make_intraday(spark, rows):
    return spark.createDataFrame(rows, INTRADAY_COLUMNS)


def make_daily(spark, rows):
    full = [(ticker, day, close, close, close, close, 1000.0) for ticker, day, close in rows]
    return spark.createDataFrame(full, DAILY_COLUMNS)


def candle(ticker, day, open_, high, low, close, volume):
    return {
        "ticker": ticker,
        "date": day,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


def metrics(ticker, day, close, prev_close, daily_return, ma_7):
    return {
        "ticker": ticker,
        "date": day,
        "close": close,
        "prev_close": prev_close,
        "daily_return": daily_return,
        "ma_7": ma_7,
    }


AAPL_DAY_1 = [
    ("AAPL", datetime(2026, 9, 1, 10, 0), 102.0, 105.0, 101.0, 104.0, 200.0, False),
    ("AAPL", datetime(2026, 9, 1, 9, 30), 100.0, 103.0, 99.0, 102.0, 100.0, False),
    ("AAPL", datetime(2026, 9, 1, 15, 59), 104.0, 106.0, 103.0, 105.0, 300.0, False),
]

AAPL_EXT_HOURS = [
    ("AAPL", datetime(2026, 9, 1, 8, 0), 90.0, 200.0, 50.0, 95.0, 1000.0, True),
]

AAPL_DAY_2 = [
    ("AAPL", datetime(2026, 9, 2, 9, 30), 105.0, 108.0, 104.0, 107.0, 150.0, False),
    ("AAPL", datetime(2026, 9, 2, 15, 59), 107.0, 109.0, 106.0, 108.0, 250.0, False),
]

MSFT_DAY_1 = [
    ("MSFT", datetime(2026, 9, 1, 9, 30), 500.0, 505.0, 498.0, 502.0, 400.0, False),
    ("MSFT", datetime(2026, 9, 1, 15, 59), 502.0, 510.0, 501.0, 509.0, 600.0, False),
]

AAPL_DAY_1_CANDLE = candle("AAPL", date(2026, 9, 1), 100.0, 106.0, 99.0, 105.0, 600.0)
AAPL_DAY_2_CANDLE = candle("AAPL", date(2026, 9, 2), 105.0, 109.0, 104.0, 108.0, 400.0)
MSFT_DAY_1_CANDLE = candle("MSFT", date(2026, 9, 1), 500.0, 510.0, 498.0, 509.0, 1000.0)


@pytest.mark.parametrize(
    ("rows", "expected"),
    [
        pytest.param(AAPL_DAY_1, AAPL_DAY_1_CANDLE, id="aapl_day_1"),
        pytest.param(AAPL_DAY_2, AAPL_DAY_2_CANDLE, id="aapl_day_2"),
        pytest.param(MSFT_DAY_1, MSFT_DAY_1_CANDLE, id="msft_day_1"),
    ],
)
def test_aggregate_daily_single_day(spark, rows, expected):
    result = aggregate_daily(make_intraday(spark, rows)).collect()

    assert len(result) == 1
    assert result[0].asDict() == expected


def test_aggregate_daily_with_ext_hours(spark):
    result = aggregate_daily(make_intraday(spark, AAPL_DAY_1 + AAPL_EXT_HOURS)).collect()

    assert len(result) == 1
    assert result[0].asDict() == AAPL_DAY_1_CANDLE


def test_aggregate_daily_combined(spark):
    result = (
        aggregate_daily(make_intraday(spark, AAPL_DAY_1 + AAPL_DAY_2 + MSFT_DAY_1))
        .orderBy("ticker", "date")
        .collect()
    )

    assert [row.asDict() for row in result] == [
        AAPL_DAY_1_CANDLE,
        AAPL_DAY_2_CANDLE,
        MSFT_DAY_1_CANDLE,
    ]


DAILY_CLOSES = [
    ("AAPL", date(2026, 9, 1), 100.0),
    ("AAPL", date(2026, 9, 2), 110.0),
    ("AAPL", date(2026, 9, 3), 121.0),
    ("MSFT", date(2026, 9, 1), 200.0),
    ("MSFT", date(2026, 9, 2), 190.0),
]


EXPECTED_METRICS = [
    metrics("AAPL", date(2026, 9, 1), 100.0, None, None, 100.0),
    metrics("AAPL", date(2026, 9, 2), 110.0, 100.0, 0.1, 105.0),
    metrics("AAPL", date(2026, 9, 3), 121.0, 110.0, 0.1, 331.0 / 3),
    metrics("MSFT", date(2026, 9, 1), 200.0, None, None, 200.0),
    metrics("MSFT", date(2026, 9, 2), 190.0, 200.0, -0.05, 195.0),
]


def test_add_daily_metrics(spark):
    result = (
        add_daily_metrics(make_daily(spark, DAILY_CLOSES))
        .select("ticker", "date", "close", "prev_close", "daily_return", "ma_7")
        .orderBy("ticker", "date")
        .collect()
    )

    for row, expected in zip(result, EXPECTED_METRICS, strict=True):
        assert row.asDict() == pytest.approx(expected)
