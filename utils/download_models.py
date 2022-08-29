import os 
import re
from pathlib import Path
from google.cloud import storage
from properties import CREDENTIALS_PATH

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
client = storage.Client()

def download_model(blob_location):
    bucket_name = re.split("/", blob_location)[2]
    prefix = blob_location.strip(f"gs://{bucket_name}/")

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            Path(blob.name).parent.mkdir(parents=True, exist_ok=True)
            with open(blob.name, 'wb') as f:
                client.download_blob_to_file(blob, f)
            print(blob.name, "Downloaded")
        return prefix
    except Exception as e :
        print(e)
        return