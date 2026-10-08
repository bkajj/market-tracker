import os
import sys

from pyspark.sql import SparkSession

if sys.platform == "win32":
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def get_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("market_tracker")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.13")
        .getOrCreate()
    )
