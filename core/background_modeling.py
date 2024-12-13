import cv2
import numpy as np

def initialize_background(camera, skip_steps=100, alpha=0.009):
    ret, frame = camera.read()
    if not ret:
        raise RuntimeError("Failed to read from camera.")

    avg_frame = np.float64(frame)
    count = 0
    while count < skip_steps:
        ret, frame = camera.read()
        if not ret:
            continue
        
        cv2.accumulateWeighted(np.float64(frame), avg_frame, alpha)
        frame_disp = cv2.convertScaleAbs(avg_frame)
        cv2.putText(frame_disp, "(BG Construction) Press 'q' to stop", 
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Background Initialization", frame_disp)
        if cv2.waitKey(1) == ord('q'):
            break
        count += 1

    cv2.destroyAllWindows()
    bg = cv2.convertScaleAbs(avg_frame)
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(bg, (21, 21), 0)
