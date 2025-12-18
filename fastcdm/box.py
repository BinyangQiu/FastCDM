import numpy as np
import cv2


def get_bboxes_from_array(img_array, colors):
    bboxes = []
    for color in colors:  # color is RGB
        # img_array is BGR (cv2 default)
        r, g, b = color
        target_bgr = np.array([b, g, r], dtype=np.uint8)

        # Create mask
        mask = cv2.inRange(img_array, target_bgr, target_bgr)
        coords = np.argwhere(mask)

        if coords.size > 0:
            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0)
            # [xmin, ymin, xmax, ymax]
            bboxes.append([int(x_min), int(y_min), int(x_max), int(y_max)])
        else:
            bboxes.append([])  # Empty list for missing token
    return bboxes
