import os
import sys

from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def get_spark() -> SparkSession:
    return (
        SparkSession.builder.master("local[*]")
        .appName("market_tracker")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.13")
        .getOrCreate()
    )
