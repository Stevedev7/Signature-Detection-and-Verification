from google.cloud import storage
import os

from properties import CREDENTIALS_PATH


def download_image(blob_location):
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
        client = storage.Client()
        bucket_name = blob_location.split("/")[2]
        bucket = client.get_bucket(bucket_name)
        prefix = "/".join(blob_location.split("/")[3:])
        file_name = blob_location.split("/")[-1]
        local_path = os.path.join("temp", file_name)
        bucket.get_blob(prefix).download_to_filename(local_path)
        return local_path
    except Exception as e:
        return {
            "error": {
                "message": e
            }
        }