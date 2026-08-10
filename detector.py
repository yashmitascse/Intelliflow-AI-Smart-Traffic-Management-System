from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE

model = YOLO(MODEL_PATH)

def detect(frame):
    results = model.predict(
        source=frame,
        conf=0.20,
        imgsz=416,
        classes=[2, 3, 5, 7],
        verbose=False
    )
    return results