import os
import pandas as pd
from dotenv import load_dotenv

# Import functions from the src directory
from src.upload_to_azure import upload_file_to_azure
from src.load_to_postgres import load_azure_csv_to_postgres

load_dotenv()


def run_scraper():
    """
    Simulation or invocation of your real OLX scraper.
    Returns a DataFrame with collected data.
    """
    print("1. Starting OLX scraper...")

    # YOUR OLX SCRAPING CODE SHOULD BE HERE
    # Creating test data for example:
    data = [
        {"id": 101, "title": "Apartment in the city center", "price": 85000, "city": "Kyiv"},
        {"id": 102, "title": "House near the forest", "price": 120000, "city": "Lviv"},
    ]

    df = pd.DataFrame(data)

    # Save locally before uploading to the cloud
    os.makedirs("data", exist_ok=True)
    csv_path = "data/olx_houses.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved locally to '{csv_path}'.")
    return csv_path


def run_pipeline():
    print("=== STARTING DATA PIPELINE ===")

    # 1. Data Collection
    local_csv = run_scraper()

    # 2. Upload raw data to Azure Blob Storage
    print("\n2. Uploading to Azure Blob Storage...")
    raw_blob_name = "raw/olx_houses.csv"
    # Call Azure upload function:
    # upload_file_to_azure(local_csv, raw_blob_name)

    # 3. Sync with Neon Postgres
    print("\n3. Syncing data with Neon Postgres...")
    load_azure_csv_to_postgres(blob_name=raw_blob_name, table_name="raw_olx_houses")

    print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_pipeline()