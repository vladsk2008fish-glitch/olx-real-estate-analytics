import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Connection String from environment variables
CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')


def upload_file_to_azure(file_path: str, container_name: str, blob_name: str = None):
    """
    Uploads a file to the specified Azure Blob Storage container.

    :param file_path: Path to the local file (e.g., 'data/olx_houses.csv')
    :param container_name: Azure container name (e.g., 'olx-data')
    :param blob_name: Destination filename in the cloud (if None, the local filename is used)
    """
    if not CONNECT_STR:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env file!")

    file = Path(file_path)
    if not file.exists():
        print(f"Error: File {file_path} not found!")
        return

    # If blob name is not specified, use the local filename
    if not blob_name:
        blob_name = f"raw/{file.name}"

    try:
        # Initialize the client
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

        # Get container client
        container_client = blob_service_client.get_container_client(container_name)

        # Create container if it does not exist in Azure Portal
        if not container_client.exists():
            container_client.create_container()
            print(f"Created new container: '{container_name}'")

        # Get blob client for uploading
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        print(f"Uploading '{file_path}' to Azure Blob Storage (container: '{container_name}', blob: '{blob_name}')...")

        with open(file_path, "rb") as data:
            # overwrite=True allows overwriting the file if it already exists in Azure
            blob_client.upload_blob(data, overwrite=True)

        print("Successfully uploaded to Azure Blob Storage!")

    except Exception as e:
        print(f"Error uploading to Azure: {e}")


if __name__ == "__main__":
    # Your Azure Portal container name
    CONTAINER = "olx-data"

    # Path to the CSV file in the data folder
    # Change 'olx_houses.csv' to your actual CSV filename
    CSV_FILE_PATH = "data/olx_houses.csv"

    upload_file_to_azure(
        file_path=CSV_FILE_PATH,
        container_name=CONTAINER
    )