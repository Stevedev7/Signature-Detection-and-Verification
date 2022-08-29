MODEL_BUCKET_LOCATION = "gs://signature-detection-verification/models" # Models should be present is gs://bucket/models/yolov5 and gs://bucket/models/vgg16
DETECTION_DESTINATION = "gs://signature-detection-verification/detections" # Stores the detected signatures in this location
CREDENTIALS_PATH = "cred.json" # Download key file for service account with GS bucket roles"
