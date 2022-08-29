import os

def check_models():
    if os.path.exists("models/vgg16/saved_model.pb") and os.path.exists("models/yolov5/best.pt") :
        return True
    return False