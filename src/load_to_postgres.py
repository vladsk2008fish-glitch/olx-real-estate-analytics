import os
import io
import pandas as pd
from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "olx-data"

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')


def get_db_engine():
    # sslmode='require' обов'язковий для зашифрованого з'єднання з Neon
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
    return create_engine(db_url)


def load_azure_csv_to_postgres(blob_name: str, table_name: str):
    if not CONNECT_STR:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING не знайдено в .env!")

    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

    print(f"Завантаження '{blob_name}' з Azure...")
    download_stream = blob_client.download_blob()
    content = download_stream.readall()

    df = pd.read_csv(io.BytesIO(content))

    engine = get_db_engine()
    print(f"Запис {len(df)} рядків у таблицю '{table_name}' в Neon Postgres...")

    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print("Успішно завантажено в хмарну базу Neon!")


if __name__ == "__main__":
    RAW_BLOB_NAME = "raw/olx_houses.csv"
    TARGET_TABLE = "raw_olx_houses"

    try:
        load_azure_csv_to_postgres(RAW_BLOB_NAME, TARGET_TABLE)
    except Exception as e:
        print(f"Помилка: {e}")