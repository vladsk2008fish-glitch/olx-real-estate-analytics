import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()  # Завантажуємо змінні з .env


class AzureBlobUploader:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("CONTAINER_NAME")

        if not self.connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING не знайдено в .env")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload_file(self, local_file_path: str, blob_name: str) -> bool:
        """Завантажує файл у хмарне сховище Azure Blob Storage."""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)

            # Створюємо контейнер, якщо його не існує
            if not container_client.exists():
                container_client.create_container()

            blob_client = container_client.get_blob_client(blob_name)

            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            print(f"Успішно завантажено {local_file_path} -> {blob_name}")
            return True
        except Exception as e:
            print(f"Помилка завантаження в Azure: {e}")
            return False