import os
import shutil
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from utils.cleanup import delete_file

from yolov5_utils import detection_fn
from utils import download_model
from utils import upload_files
from utils import check_models
from utils import download_image
from utils import verify

from properties import DETECTION_DESTINATION
from properties import MODEL_BUCKET_LOCATION

app = FastAPI()

#Application startup script. This Function Downloads the models if they are not present.

@app.on_event("startup")
async def startup_event():
    if not check_models():
        download_model(MODEL_BUCKET_LOCATION)
    else:
        print("Models are already present")

@app.on_event("shutdown")
def shutdown_event():
    try:
        shutil.rmtree("results")
    except Exception as e:
        print(e.args[0])
    

class BucketLocation(BaseModel):
    location: str = Field(description="GCS bucket location to the document image.")
    def __getitem__(self, item):
        return getattr(self, item)

@app.get("/")
async def home():
    return {"data": "Home dir"}

# Signature detection route

@app.post("/detect")
def sig_detect(document: BucketLocation = Body(embed=True)):
    document_name = document.location.split("/")[-1].split(".")[0]
    doc = download_image(document.location)
    if os.path.exists(doc):
        detections = detection_fn(doc)
        # Delete the image from temp file
        delete_file(doc)
        # Checking if the signatures are detected
        if "crops" in os.listdir(detections):
            bucket_location = upload_files(os.path.join(detections, "crops", "DLSignature"), document_name, DETECTION_DESTINATION)

            return {
                "detections": bucket_location
            }
        return {
            "message": "Signature not detected"
        }
    else :
        return {
            "error": {
                "message" : doc.error.message or "Something went wrong"
            }
        }

# Signature verification route

@app.post("/verify")
def sig_verify(sign_1: BucketLocation = Body(embed=True), sign_2: BucketLocation = Body(embed=True)):
    signs = [os.path.join("temp",_.split("/")[-1]) for _ in [sign_1.location, sign_2.location]]
    for signature in [sign_1.location, sign_2.location]:
        sign = download_image(signature)
    
    score = verify(signs[0], signs[1]) # Score > 8 can be assumed as similar signatures
    # Clean up
    for _ in signs:
        delete_file(f"{_}")
    return {
        "score": float(score)
    }