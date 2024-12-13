
import cv2

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
    sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    threshold_value = 100
    _, threshold_result = cv2.threshold(sobel_combined, threshold_value, 255, cv2.THRESH_BINARY)

    return cv2.GaussianBlur(gray, (21, 21), 0), sobel_combined, threshold_result, cv2.GaussianBlur(gray, (21, 21), 0)

def draw_bounding_box(frame, box_coords, color=(0, 255, 0)):
    x, y, w, h = box_coords
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)