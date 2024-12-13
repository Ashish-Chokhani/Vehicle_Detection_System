import cv2
import numpy as np
from core.utilities import draw_bounding_box

def detect_motion(prev_frame, current_frame, vehicles, cutoff, dist_threshold, update_fn, crop_coords, display_frame):

    frame_delta = cv2.absdiff(prev_frame, current_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=4)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < cutoff:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        bounding_area = w * h
        if bounding_area / area > 1.8:
            continue

        found = False
        for vehicle in vehicles:
            if np.linalg.norm(vehicle['position'] - np.array([x, y])) < dist_threshold:
                found = True
                if bounding_area > vehicle['area']:
                    update_fn(bounding_area, vehicle['area'])
                    vehicle['area'] = bounding_area
                vehicle['position'] = np.array([x, y])
                break
        
        if not found:
            vehicles.append({"position": np.array([x, y]), "area": bounding_area})
            update_fn(bounding_area)

        draw_bounding_box(display_frame, (x, y, w, h))

    return thresh
