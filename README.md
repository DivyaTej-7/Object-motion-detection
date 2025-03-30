# Object Detection and Tracking with OpenCV

## Overview
This project is a real-time object detection and tracking system using OpenCV. The script captures frames from a webcam, detects moving objects, and logs their coordinates into a CSV file. It also calculates distances between detected objects and handles frame reading errors.

## Features
- Captures video feed using OpenCV.
- Detects and tracks moving objects.
- Logs object details (coordinates, size, and distance to the next object) into a CSV file.
- Handles errors with retries for robustness.
- Stops execution after a set duration or manual termination.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install opencv-python imutils
```

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Run the script:
   ```bash
   python ex2d4-4imp.py
   ```
3. The detected object details are saved in `object_coordinates.csv`.

## Output
- The script will display the live camera feed with detected objects marked.
- The terminal will print detection messages.
- A CSV file (`object_coordinates.csv`) will store frame-wise object data.

## Stopping the Script
- The script will run for 10 seconds by default.
- Press `q` to manually exit.

## Issues and Contributions
Feel free to raise issues or contribute to this project by submitting pull requests.

## License
This project is licensed under the MIT License.
