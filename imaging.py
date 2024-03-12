import cv2
import torch
from simulator import Simulator
import numpy as np
from anomalies_img import FrameAnomalyDetector
import pandas as pd

class Imaging:
    cap = None
    model = None
    initialized = False
    columns = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
           'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
           'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
           'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
           'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
           'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
           'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
           'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
           'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
           'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
           'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
           'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
           'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    index = 0

    @staticmethod
    def initialize():
        if Imaging.initialized:
            return
        else:
            Imaging.initialized = True
            Imaging.cap = cv2.VideoCapture(0)
            Imaging.cap.release()
            Imaging.cap = cv2.VideoCapture(0)
            Imaging.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')
    # Function to generate frames from webcam
    @staticmethod
    def generate_frames():
        while True:
            ret, frame = Imaging.cap.read()
            if not ret:
                continue
            model_results = Imaging.model(frame)
            if Imaging.index % 80 == 0:
                df_res = model_results.pandas().xyxy[0]
                obj_detected = df_res[["name"]].values
                Simulator.update_people(np.count_nonzero(obj_detected == "person"))
                df_detected = pd.DataFrame(data = np.zeros((1, 80)),columns=Imaging.columns)
                for i in range(len(df_res)):
                    df_detected[df_res.iloc[i]["name"]] = df_detected[df_res.iloc[i]["name"]] + 1
                FrameAnomalyDetector.update_detected(df_detected)
                Imaging.index = 0
            Imaging.index += 1
            ret, buffer = cv2.imencode('.jpg', model_results.render()[0])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')