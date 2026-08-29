import os
import io
import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "olx-data"


def read_blob_to_dataframe(blob_name: str) -> pd.DataFrame:
    """
    Reads a CSV file directly from Azure Blob Storage into a Pandas DataFrame.
    """
    if not CONNECT_STR:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env!")

    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

    print(f"Reading '{blob_name}' from Azure Blob Storage...")

    # Download blob content into memory
    download_stream = blob_client.download_blob()
    content = download_stream.readall()

    # Convert bytes into Pandas DataFrame
    df = pd.read_csv(io.BytesIO(content))
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Example data cleaning logic.
    """
    print("Cleaning and processing data...")
    # Add your data transformation logic here (e.g., handling missing values, changing types)
    df = df.drop_duplicates()
    return df


if __name__ == "__main__":
    RAW_BLOB_NAME = "raw/olx_houses.csv"

    try:
        df_raw = read_blob_to_dataframe(RAW_BLOB_NAME)
        print("\nRaw Data Sample:")
        print(df_raw.head())

        df_cleaned = clean_data(df_raw)
        print("\nCleaned Data Sample:")
        print(df_cleaned.head())

    except Exception as e:
        print(f"Error reading/processing blob: {e}")