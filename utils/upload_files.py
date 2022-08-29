from datetime import datetime
import os
import shutil
from google.cloud import storage

from .cleanup import delete_file

from properties import CREDENTIALS_PATH

def upload_files(path, doc_name, blob_location):
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
        client = storage.Client()
        bucket_name = blob_location.split("/")[2]
        bucket = client.get_bucket(bucket_name)
        prefix = "/".join(blob_location.split("/")[3:])
        images = os.listdir(path)
        TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")
        
        for image in images:
            file_extension = image.split(".")[-1]
            index = images.index(image)
            blob_name = os.path.join(f"{TIMESTAMP}{doc_name}_{index + 1}.{file_extension}")
            blob = bucket.blob(os.path.join(prefix, doc_name, blob_name))
            blob.upload_from_filename(os.path.join(path, image))
        return {
            "detections": f"gs://{os.path.join(bucket_name, prefix, doc_name)}"
        }
            
    except Exception as e :
        return {
            "error": {
                "message": e
            }
        }

