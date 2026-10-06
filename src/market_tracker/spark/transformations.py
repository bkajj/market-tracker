from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def aggregate_daily(prices: DataFrame) -> DataFrame:
    return (
        prices.withColumn("date", F.to_date(F.col("timestamp")))
        .filter(~F.col("ext_hours"))
        .groupBy("ticker", "date")
        .agg(
            F.min_by("open", "timestamp").alias("open"),
            F.max("high").alias("high"),
            F.min("low").alias("low"),
            F.max_by("close", "timestamp").alias("close"),
            F.sum("volume").alias("volume"),
        )
    )
