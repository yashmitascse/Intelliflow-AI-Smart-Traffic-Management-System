import cv2
from ultralytics import YOLO

from config import MODEL_PATH, VIDEO_PATH
from analytics import traffic_density
from traffic_signal import get_signal_time
from server import update_traffic
from alerts import generate_alert

# ==============================
# SETTINGS
# ==============================

CONFIDENCE = 0.20
IMAGE_SIZE = 416
FRAME_SKIP = 3

VEHICLE_CLASSES = [2, 3, 5, 7]

# ==============================
# LOAD MODEL
# ==============================

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded.")

# ==============================
# OPEN VIDEO
# ==============================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open video.")
    exit()

# ==============================
# VARIABLES
# ==============================

frame_number = 0
last_frame = None

vehicle_count = 0
density = "LOW"
signal_time = 15

# ==============================
# MAIN LOOP
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    # ==============================
    # RUN YOLO + BYTE TRACK
    # ==============================

    if frame_number % FRAME_SKIP == 0:

        results = model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE,
            imgsz=IMAGE_SIZE,
            classes=VEHICLE_CLASSES,
            verbose=False
        )

        result = results[0]

        # ==============================
        # COUNT CURRENT VEHICLES
        # ==============================

        if (
            result.boxes is not None
            and result.boxes.id is not None
        ):

            ids = result.boxes.id.int().cpu().tolist()

            vehicle_count = len(set(ids))

            print(
                f"Frame {frame_number} | "
                f"Vehicles: {vehicle_count} | "
                f"IDs: {ids}"
            )

        else:

            vehicle_count = 0

            print(
                f"Frame {frame_number} | "
                f"No vehicles detected"
            )

        # ==============================
        # TRAFFIC ANALYSIS
        # ==============================

        density = traffic_density(vehicle_count)

        signal_time = get_signal_time(vehicle_count)

        # ==============================
        # ALERT
        # ==============================

        alert = generate_alert(
            vehicle_count,
            density
        )

        # ==============================
        # UPDATE FLASK
        # ==============================

        update_traffic(
            vehicle_count,
            density,
            signal_time
        )

        # ==============================
        # TERMINAL OUTPUT
        # ==============================

        print("=" * 50)
        print(f"Vehicle Count   : {vehicle_count}")
        print(f"Traffic Density : {density}")
        print(f"Green Signal    : {signal_time} sec")
        print(f"Alert           : {alert['message']}")
        print(f"Recommendation  : {alert['recommendation']}")
        print("=" * 50)

        # ==============================
        # DRAW DETECTIONS
        # ==============================

        last_frame = result.plot()

    # ==============================
    # DISPLAY
    # ==============================

    if last_frame is not None:

        cv2.imshow(
            "IntelliFlow AI - ByteTrack",
            last_frame
        )

    else:

        cv2.imshow(
            "IntelliFlow AI - ByteTrack",
            frame
        )

    # ==============================
    # ESC TO EXIT
    # ==============================

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==============================
# CLEANUP
# ==============================

cap.release()
cv2.destroyAllWindows()

print("IntelliFlow AI stopped.")