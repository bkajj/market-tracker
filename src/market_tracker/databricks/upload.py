import logging
from pathlib import Path

from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def upload_to_bronze(
    databricks_basepath: str = "/Volumes/workspace/market_bronze/raw",
    data_path: str = "data",
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
        file_path = f"{databricks_basepath}/{p.relative_to(root).as_posix()}"
        with open(p, "rb") as f:
            w.files.upload(file_path=file_path, contents=f, overwrite=True)
            logger.info(f"SENT {file_path}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    upload_to_bronze()
