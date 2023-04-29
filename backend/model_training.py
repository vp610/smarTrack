import os
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(data='./datasets/package_detection-1/data.yaml', epochs=10, name='yolov8n_boxes', device=0)
