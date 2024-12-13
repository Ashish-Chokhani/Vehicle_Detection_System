import cv2
import numpy as np
from core.utilities import preprocess_frame
from core.background_modeling import initialize_background
from core.motion_detection import detect_motion

class VehicleDetection:

    def __init__(self, config):
        self.config = config
        self.camera = cv2.VideoCapture(config["STREAM_URL"])        
        self.skip_steps = config["SKIP_STEPS"]
        self.cutoff = config["CUTOFF_AREA"]
        self.dist_threshold = config["DIST_THRESHOLD"]
        self.thresholds = config["THRESHOLDS"]
        self.bg = None
        self.vehicles = []
        self.type_counts = {f"type{i}": 0 for i in range(1, 5)}
        self.crop_coords = [1, 1, config["FRAME_WIDTH"], config["FRAME_HEIGHT"]]

        self.output_video = None
        self.sobel_video = None
        self.threshold_video = None
        self.fps = config.get("FPS", 20)
        self.output_file = "output_video.mp4"
        self.sobel_file =  "sobel_output.mp4"
        self.gaussian_file =  "gaussian_output.mp4"
        self.threshold_file =  "threshold_output.mp4"
        self.dilation_file =  "dilation_output.mp4"

    def configure(self):
        self._select_region_of_interest()
        self._initialize_background()

    def _select_region_of_interest(self):
        self.first_click = True

        def region_selector(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if self.first_click:
                    self.start_point = (x, y)
                    self.first_click = False
            elif event == cv2.EVENT_LBUTTONUP:
                self.crop_coords = [self.start_point[0], self.start_point[1], x, y]
                self.first_click = True
                cv2.rectangle(self.frame, self.start_point, (x, y), (0, 255, 0), 2)
            if not self.first_click:
                ret, frame = self.camera.read()
                self.frame = frame[min(self.crop_coords[1], self.crop_coords[3]):max(self.crop_coords[1], self.crop_coords[3]),
                           min(self.crop_coords[0], self.crop_coords[2]):max(self.crop_coords[0], self.crop_coords[2])]
                cv2.rectangle(self.frame, (self.start_point), (x, y), (255, 0, 0), 2)

        ret, self.frame = self.camera.read()
        if ret:
            cv2.namedWindow("Select ROI")
            cv2.setMouseCallback("Select ROI", region_selector)
            while True:
                text = "(CONFIG_MODE) Drag mouse to define ROI and press q when complete"
                cv2.putText(self.frame, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("Select ROI", self.frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            cv2.destroyAllWindows()
        else:
            frame_height, frame_width = self.frame.shape[:2]
            self.crop_coords = [0, 0, frame_width, frame_height]

    def _initialize_background(self):
        self.bg = initialize_background(self.camera, self.skip_steps)

    def _setup_video_writer(self, frame_width, frame_height):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output_video = cv2.VideoWriter(self.output_file, fourcc, self.fps, (frame_width, frame_height))
        self.sobel_video = cv2.VideoWriter(self.sobel_file, fourcc, self.fps, (frame_width, frame_height), isColor=False)
        self.threshold_video = cv2.VideoWriter(self.threshold_file, fourcc, self.fps, (frame_width, frame_height), isColor=False)
        self.gaussian_video = cv2.VideoWriter(self.gaussian_file, fourcc, self.fps, (frame_width, frame_height), isColor=False)
        self.dilation_video = cv2.VideoWriter(self.dilation_file, fourcc, self.fps, (frame_width, frame_height), isColor=False)

    def run(self):
        frame_index = 0
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            cropped_frame = frame[
                min(self.crop_coords[1], self.crop_coords[3]):max(self.crop_coords[1], self.crop_coords[3]),
                min(self.crop_coords[0], self.crop_coords[2]):max(self.crop_coords[0], self.crop_coords[2]),
            ]

            processed_frame, sobel_combined, threshold_result, gaussian_result = preprocess_frame(cropped_frame)
            frame_index += 1

            reference_frame = (
                self.bg[min(self.crop_coords[1], self.crop_coords[3]):max(self.crop_coords[1], self.crop_coords[3]),
                        min(self.crop_coords[0], self.crop_coords[2]):max(self.crop_coords[0], self.crop_coords[2])]
                if self.bg is not None
                else processed_frame
            )

            dilation = detect_motion(
                reference_frame,
                processed_frame,
                self.vehicles,
                self.cutoff,
                self.dist_threshold,
                self.update_vehicle_types,
                self.crop_coords,
                cropped_frame
            )

            if self.output_video is None:
                frame_height, frame_width = cropped_frame.shape[:2]
                self._setup_video_writer(frame_width, frame_height)

            self.output_video.write(cropped_frame)
            self.sobel_video.write(sobel_combined)
            self.threshold_video.write(threshold_result)
            self.gaussian_video.write(gaussian_result)
            self.dilation_video.write(dilation)

            self.display_frame(cropped_frame)
            if cv2.waitKey(50) == ord("q"):
                break

        self.camera.release()
        self.output_video.release()
        self.sobel_video.release()
        self.threshold_video.release()
        self.gaussian_video.release()
        self.dilation_video.release()
        cv2.destroyAllWindows()

    def update_vehicle_types(self, new_area, old_area=None):
        def get_type(area):
            if area < self.thresholds["low"]:
                return "type1"
            elif area < self.thresholds["mid"]:
                return "type2"
            elif area < self.thresholds["high"]:
                return "type3"
            else:
                return "type4"

        new_type = get_type(new_area)

        if old_area is not None:
            old_type = get_type(old_area)
            if new_type != old_type:
                if self.type_counts[old_type] > 0:
                    self.type_counts[old_type] -= 1
                self.type_counts[new_type] += 1
        else:
            self.type_counts[new_type] += 1

    def display_frame(self, frame):
        total_count = f"Total: {len(self.vehicles)}"
        type_counts = ", ".join([f"{k}: {v}" for k, v in self.type_counts.items()])
        cv2.putText(frame, total_count, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, type_counts, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Vehicle Detection", frame)



