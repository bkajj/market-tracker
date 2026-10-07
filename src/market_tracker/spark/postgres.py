from pyspark.sql import DataFrame, SparkSession

from market_tracker.db.engine import get_connection_url
from market_tracker.db.models import DailyPrice, IntradayPrice
from market_tracker.spark.transformations import add_daily_metrics, aggregate_daily


def _jdbc_options() -> dict[str, str]:
    url_data = get_connection_url()
    return {
        "url": f"jdbc:postgresql://{url_data.host}:{url_data.port}/{url_data.database}",
        "user": url_data.username,
        "password": url_data.password,
        "driver": "org.postgresql.Driver",
    }


def read_prices(spark: SparkSession) -> DataFrame:
    return (
        spark.read.format("jdbc")
        .options(**_jdbc_options())
        .option("dbtable", IntradayPrice.__tablename__)
        .load()
    )


def write_daily_prices(df: DataFrame) -> None:
    (
        df.write.format("jdbc")
        .options(**_jdbc_options())
        .option("dbtable", DailyPrice.__tablename__)
        .option("truncate", "true")
        .mode("overwrite")
        .save()
    )


if __name__ == "__main__":
    from market_tracker.spark.session import get_spark

    spark = get_spark()
    df = read_prices(spark)
    daily = aggregate_daily(df)
    add_daily_metrics(daily).orderBy("ticker", "date").show()
    spark.stop()
