# Vehicle Detection and Tracking System

**Authors**: Ashish Chokhani (2021102016), Ishit Bansal (2021101083)  
**Guide**: Dr. Anoop Namboodiri  
**Institute**: International Institute of Information Technology Hyderabad  

---

## 📋 Project Overview

This project focuses on real-time **Vehicle Detection and Tracking** to enhance traffic flow analysis. Using advanced digital image processing techniques, we aim to improve the accuracy of vehicle detection, classification, and tracking for efficient traffic monitoring.

Key features include:
- Detection and tracking of vehicles across predefined regions of interest.
- Classification of vehicles into four categories: Bicycles/Motorcycles, Cars, Pickup/Minibuses, and Buses/Trucks/Trailers.
- GUI for configuring parameters and visualizing results.

---

## 👨‍💻 Directory Structure

```
├── DIP_Project_Proposal.pdf   # Initial project proposal
├── GUI                        # GUI-related code
│   └── gui.py                 # GUI implementation
├── Report.pdf                 # Final project report
├── core                       # Core implementation files
│   ├── background_modeling.py # Background modeling logic
│   ├── kalman_filter.py       # Kalman filter for vehicle tracking
│   ├── motion_detection.py    # Motion detection algorithms
│   ├── utilities.py           # Helper functions
│   └── vehicle_detection.py   # Vehicle detection methods
├── data                       # Dataset (video clips)
│   ├── 1.mp4
│   ├── 2.mp4
│   ├── 3.mp4
│   ├── 4.mp4
│   ├── 5.mp4
│   └── video.mp4
├── main.py                    # Entry point for the application
└── requirements.txt           # Python dependencies
```

---

## 🚀 Features

### 1. Vehicle Detection
- **Background Modeling**: Moving average method with Gaussian smoothing for robust background subtraction.
- **Noise Reduction**: Gaussian blur applied to grayscale frames.
- **Object Detection**: Contours and bounding boxes highlight detected vehicles.

### 2. Vehicle Tracking
- **Nearest Neighbor Approach**: Tracks vehicles between frames based on bounding box positions.
- **Dynamic ROI Selection**: Focuses detection within user-defined regions of interest.

### 3. Vehicle Classification
Classifies detected vehicles based on their size into:
- Type 1: Bicycle, Motorcycle
- Type 2: Car
- Type 3: Pickup, Minibus
- Type 4: Bus, Truck, Trailer

### 4. GUI
Interactive GUI features:
- Video clip selection
- Configurable parameters (e.g., ROI, area thresholds, skip steps)
- Real-time detection and visualization

---

## How to Run

### Prerequisites
1. Python 3.10 or above
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Steps
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_directory>
   ```
2. Run the application:
   ```bash
   python main.py
   ```

3. Use the GUI to:
   - Select video clips
   - Configure detection parameters
   - Start the vehicle detection process

---

## Results and Accuracy

- Improved vehicle detection and tracking through optimized algorithms.
- Classification accuracy showcased using a confusion matrix in the report.
- Overcame challenges like lighting variations, occlusions, and high frame rates.

---

## Challenges Faced

- Difficulty tracking vehicles across lanes.
- Shadows and inconsistent lighting affecting detection.
- Misclassification of closely grouped vehicles.

---

## Future Improvements

- Incorporate deep learning models for enhanced detection accuracy.
- Optimize processing speed for higher frame rates.
- Add more robust vehicle classification features.

---


## 🚨 Don't forget to check out this amazing report for more insights into the project!
- [Project Presentation (PDF)](https://github.com/Ashish-Chokhani/GrammarML-EduAssessment/blob/main/docs/BTP_report2.pdf)

## 🤝 Contributions
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.


## References

1. Tourani, A., & Shahbahrami, A. (2015). *Vehicle counting method based on digital image processing algorithms*. 2nd International Conference on Pattern Recognition and Image Analysis (IPRIA).
2. Pancharatnam, M., & Sonnadara, U. (2008). *Vehicle Counting and Classification from a Traffic Scene*.

---

## License

This project is licensed under the Team Visionary.
