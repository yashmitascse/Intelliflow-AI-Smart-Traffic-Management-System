def track(model, frame, confidence=0.20):
    results = model.track(
        source=frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=confidence,
        imgsz=416,
        classes=[2, 3, 5, 7],
        verbose=False
    )

    return results