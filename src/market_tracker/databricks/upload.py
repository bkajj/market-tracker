import logging
from pathlib import Path

from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)

DATABRICKS_BASEPATH = "/Volumes/workspace/market_bronze/raw"


def upload_file(
    w: WorkspaceClient,
    local_path: str,
    data_path: str,
    databricks_basepath: str = DATABRICKS_BASEPATH,
):
    local_path = Path(local_path)
    root = Path(f"{data_path}/raw")
    file_path = f"{databricks_basepath}/{local_path.relative_to(root).as_posix()}"
    with open(local_path, "rb") as f:
        w.files.upload(file_path=file_path, contents=f, overwrite=True)
        logger.info(f"SENT {file_path}")


def backfill_bronze(
    data_path: str = "data",
    databricks_basepath: str = DATABRICKS_BASEPATH,
    date: str = "*",
    interval: str = "*",
    ticker: str = "*",
):
    w = WorkspaceClient()

    root = Path(f"{data_path}/raw")
    pattern = f"intraday/interval={interval}/ticker={ticker}/date={date}.json"
    files = list(root.glob(pattern))
    if not files:
        logger.warning("no local files detected to upload")

    for p in files:
        upload_file(w, p, data_path, databricks_basepath)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    backfill_bronze()
