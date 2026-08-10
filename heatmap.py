import cv2
import numpy as np

# Create an empty heatmap
heatmap = None


def update_heatmap(frame, boxes):
    global heatmap

    # Create heatmap on first frame
    if heatmap is None:
        heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)

    # Add "heat" where vehicles are detected
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        cv2.circle(
            heatmap,
            (center_x, center_y),
            25,
            1,
            -1
        )

    return heatmap


def get_heatmap(frame):
    global heatmap

    if heatmap is None:
        return frame

    # Normalize values
    normalized = cv2.normalize(
        heatmap,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    ).astype(np.uint8)

    # Apply color map
    colored = cv2.applyColorMap(
        normalized,
        cv2.COLORMAP_JET
    )

    # Overlay heatmap on original frame
    output = cv2.addWeighted(
        frame,
        0.6,
        colored,
        0.4,
        0
    )

    return output