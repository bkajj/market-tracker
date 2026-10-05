from pyspark.sql import DataFrame, SparkSession

from market_tracker.db.engine import get_connection_url
from market_tracker.db.models import IntradayPrice


def read_prices(spark: SparkSession) -> DataFrame:
    url_data = get_connection_url()
    return (
        spark.read.format("jdbc")
        .option(
            "url",
            f"jdbc:postgresql://{url_data.host}:{url_data.port}/{url_data.database}",
        )
        .option("dbtable", IntradayPrice.__tablename__)
        .option("user", url_data.username)
        .option("password", url_data.password)
        .option("driver", "org.postgresql.Driver")
        .load()
    )


if __name__ == "__main__":
    from market_tracker.spark.session import get_spark

    spark = get_spark()
    df = read_prices(spark)
    df.printSchema()
    df.show(5)
    spark.stop()
