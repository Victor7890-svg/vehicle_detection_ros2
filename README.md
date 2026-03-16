# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

**Student Name:** Caijialiang  
**Student ID:** 22100304d  
**Date:** 2026-03-16

## 1. Overview
This project implements a real-time vehicle detection pipeline using ROS2 and YOLOv8. It reads a compressed image topic from a converted rosbag, performs inference to detect vehicles (cars, buses, trucks), and displays the annotated results in an OpenCV window.

## 2. Detection Method (Q3.1 — 2 marks)
I chose **YOLOv8 (nano)** as the detection model because it offers an excellent balance between speed and accuracy, making it suitable for near-real-time processing. The model is pre-trained on the COCO dataset, which includes the vehicle classes of interest (car: class 2, bus: class 5, truck: class 7). Using a lightweight variant ensures that the pipeline can run on modest hardware while still producing reliable detections.

## 3. Repository Structure
vehicle_detection_pkg/
├── launch/
│ └── detection_launch.py # Launches rosbag player and detection node
├── vehicle_detection_pkg/
│ ├── init.py
│ └── detection_node.py # Main detection node
├── package.xml # Package manifest
├── setup.py # Python package configuration
├── setup.cfg
├── resource/
└── test/ # Unit tests (auto-generated)

## 4. Prerequisites
- **OS:** Ubuntu 24.04 (via WSL2 on Windows 11)
- **ROS2 Distribution:** Jazzy
- **Python:** 3.12
- **Key Python Libraries:**
  - opencv-python (for image display and processing)
  - ultralytics (YOLOv8)
  - numpy

## 5. How to Run (Q3.1 — 2 marks)

```bash
cd ~/ros2_ws/src
git clone https://github.com/Victor7890-svg/vehicle_detection_ros2.git
python3 -m venv ~/ros2_venv --system-site-packages
source ~/ros2_venv/bin/activate
pip install opencv-python ultralytics numpy
cd ~/ros2_ws
colcon build
source install/setup.bash
pip install rosbags
rosbags-convert --src <your_ros1_bag.bag> --dst converted_bag
ros2 launch vehicle_detection_pkg detection_launch.py
```
Video Demonstration (Q3.2)
Video Link: https://youtu.be/T30NlouznEY

Reflection & Critical Analysis (Q3.3)

(a) What Did You Learn? 
Through this project, I gained two key technical skills:

ROS2 node development: I learned how to create a Python subscriber for compressed image topics, handle message conversion using cv_bridge and OpenCV, and structure a ROS2 package with proper launch files.

Integrating deep learning with ROS: I practiced loading a pre-trained YOLO model and running inference in real-time within a ROS2 pipeline, including filtering results to specific classes and overlaying annotations.

(b) How Did You Use AI Tools? 
I used ChatGPT extensively for debugging and code generation. The benefits included rapid troubleshooting of build errors (e.g., missing dependencies, launch file issues) and getting boilerplate code for ROS2 nodes. However, limitations were that AI sometimes provided outdated or ROS1-specific syntax, requiring manual verification against official documentation. Additionally, it could not help with environment-specific issues like WSL2 GUI configuration.

(c) How to Improve Accuracy? 
Two concrete strategies to improve detection accuracy:

Use a larger YOLO model: Switching from yolov8n.pt (nano) to yolov8m.pt (medium) or yolov8l.pt (large) would increase accuracy, especially for small or distant vehicles, at the cost of slower inference. This trade-off could be acceptable if real-time performance is not critical.

Fine-tune on domain-specific data: Training the model on a dataset of images from the same camera perspective (e.g., dashboard cameras) would adapt it to the specific visual conditions (lighting, road types, vehicle angles), significantly improving detection in this context.

(d) Real-World Challenges
Deploying this pipeline on an actual drone in real time would face:

Computational constraints: Drones have limited onboard processing power and battery life. Running a deep learning model may require an edge accelerator (e.g., NVIDIA Jetson) or model compression techniques like quantization or pruning.

Latency and synchronization: Image capture, transmission, and inference must occur within strict timing windows (e.g., 30–50 ms) to support real-time control. Delays could cause the drone to react to outdated information, leading to unstable flight or missed obstacles.
