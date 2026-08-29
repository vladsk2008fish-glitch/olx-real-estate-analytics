from src import AzureBlobUploader

def main():
    uploader = AzureBlobUploader()
    uploader.upload_file(
        local_file_path="data/sample.csv",
        blob_name="raw/sample_2026_08.csv"
    )

if __name__ == "__main__":
    main()