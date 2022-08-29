import glob, os, shutil
from yolov5 import detect

from .util import resize_images

YOLO_RESULT = 'results/yolov5/'
YOLO_WEIGHTS = 'models/yolov5/best.pt'

def signature_detection(img):
    result=detect.run(source=img, weights=YOLO_WEIGHTS, imgsz=640, conf_thres=0.25, iou_thres=0.45, save_txt=True, save_conf=True, save_crop=True, nosave=True, classes=1, project=YOLO_RESULT)


    latest_detection = max(glob.glob(os.path.join(YOLO_RESULT, '*/')), key=os.path.getmtime)
    return latest_detection