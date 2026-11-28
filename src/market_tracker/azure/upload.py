import logging
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import FileSystemClient

logger = logging.getLogger(__name__)


def create_adls_client():
    return FileSystemClient(
        account_url=os.environ["AZURE_ADLS_URL"],
        file_system_name="raw",
        credential=DefaultAzureCredential(),
    )


def upload_to_adls(fs_client: FileSystemClient, local_path: str, data_path: str):
    local_path = Path(local_path)
    root = Path(f"{data_path}/raw")
    file_path = local_path.relative_to(root).as_posix()

    file_client = fs_client.get_file_client(file_path)
    with open(local_path, "rb") as data:
        file_client.upload_data(data, overwrite=True)
        logger.info(f"SENT TO AZURE {file_path}")
