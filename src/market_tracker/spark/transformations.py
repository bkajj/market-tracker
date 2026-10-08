from pyspark.sql import DataFrame, Window
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


def add_daily_metrics(daily: DataFrame) -> DataFrame:
    window = Window.partitionBy("ticker").orderBy("date")
    ma_window = window.rowsBetween(-6, Window.currentRow)
    return (
        daily.withColumn("prev_close", F.lag("close").over(window))
        .withColumn("daily_return", (F.col("close") - F.col("prev_close")) / F.col("prev_close"))
        .withColumn("ma_7", F.avg("close").over(ma_window))
    )
