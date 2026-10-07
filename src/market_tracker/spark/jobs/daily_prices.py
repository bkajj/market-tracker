from market_tracker.spark.postgres import read_prices, write_daily_prices
from market_tracker.spark.session import get_spark
from market_tracker.spark.transformations import add_daily_metrics, aggregate_daily


def main() -> None:
    spark = get_spark()
    try:
        intraday = read_prices(spark)
        candles = aggregate_daily(intraday)
        daily_prices = add_daily_metrics(candles)
        write_daily_prices(daily_prices)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
