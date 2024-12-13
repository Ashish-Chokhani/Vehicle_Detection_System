import tkinter as tk
from core.vehicle_detection import VehicleDetection


class VehicleDetectionGUI:
    def __init__(self):
        self.vehicle_det_obj = None
        self.selectClip = None
        self.skip_steps = None
        self.cutoff = None
        self.threshold_lower = None
        self.threshold_middle = None
        self.threshold_higher = None

    def start_detection(self):
        self.vehicle_det_obj.run()

    def configure(self):
        config = {
            "STREAM_URL": f"./data/{self.selectClip.get()}.mp4",
            "SKIP_STEPS": self.skip_steps.get(),  
            "CUTOFF_AREA": self.cutoff.get(), 
            "DIST_THRESHOLD": 50, 
            "THRESHOLDS": {
                "low": self.threshold_lower.get(), 
                "mid": self.threshold_middle.get(),  
                "high": self.threshold_higher.get(),  
            },
            "FRAME_WIDTH": 100000, 
            "FRAME_HEIGHT": 100000 
        }
        self.vehicle_det_obj = VehicleDetection(config)
        self.vehicle_det_obj.configure()

    def run_gui(self):
        window = tk.Tk(className="Vehicle Counter")
        rw = 0

        tk.Label(text="Clip Selection: ").grid(row=rw, column=0)
        self.selectClip = tk.IntVar(value=1)
        for i in range(1, 6):
            tk.Radiobutton(window, text=f"Clip {i}", variable=self.selectClip, value=i).grid(row=rw, column=i)

        rw += 1
        tk.Label(text="Skip Steps: ").grid(row=rw, column=0)
        self.skip_steps = tk.Scale(window, from_=100, to=200, orient=tk.HORIZONTAL)
        self.skip_steps.grid(row=rw, column=1)
        rw += 1

        tk.Label(text="Cutoff Area: ").grid(row=rw, column=0)
        self.cutoff = tk.Scale(window, from_=2000, to=10000, orient=tk.HORIZONTAL, resolution=500)
        self.cutoff.grid(row=rw, column=1)
        rw += 1

        tk.Label(text="Lower Threshold: ").grid(row=rw, column=0)
        self.threshold_lower = tk.Scale(window, from_=10000, to=50000, orient=tk.HORIZONTAL, resolution=5000)
        self.threshold_lower.grid(row=rw, column=1)
        rw += 1

        tk.Label(text="Middle Threshold: ").grid(row=rw, column=0)
        self.threshold_middle = tk.Scale(window, from_=35000, to=80000, orient=tk.HORIZONTAL, resolution=5000)
        self.threshold_middle.grid(row=rw, column=1)
        rw += 1

        tk.Label(text="Higher Threshold: ").grid(row=rw, column=0)
        self.threshold_higher = tk.Scale(window, from_=60000, to=100000, orient=tk.HORIZONTAL, resolution=5000)
        self.threshold_higher.grid(row=rw, column=1)
        rw += 1

        configButton = tk.Button(window, text="Configure", command=self.configure)
        configButton.grid(row=rw, column=3)

        startButton = tk.Button(window, text="Start", command=self.start_detection)
        startButton.grid(row=rw, column=4)
        window.mainloop()



