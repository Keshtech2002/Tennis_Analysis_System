# Tennis Match Analysis System

A computer vision project built to transform raw tennis match footage into tactical, spatial, and performance intelligence. Instead of simply watching a video, this system tries to understand what happened on the court: where the players were, where the ball was hit, how fast the shot travelled, and how the motion evolved over time.

This project sits at the intersection of object detection, multi-object tracking, court geometry, and sports analytics. It takes a video as input, detects players and the ball, reconstructs a tennis court in a normalized mini-court view, and then computes meaningful match-level insights from the movement patterns.

---

## Why this project exists

Traditional video analysis is often descriptive: it records footage, but does not really understand the game. This project is a step toward a different idea.

The goal is simple but ambitious:

- detect players and the ball in a tennis frame
- track those objects across time
- estimate court keypoints and reconstruct court geometry
- map player and ball positions onto a mini-court coordinate system
- convert motion into measurable quantities such as speed and distance
- visualize the result as an annotated output video with analysis overlays

The result is not just a processed video. It is a pipeline for understanding tennis movement and shot dynamics from a single camera feed.

---

## The Workflow

The workflow begins with a match video. A player detection model identifies athletes, while a dedicated ball detector identifies the tennis ball. This gives the system a frame-by-frame understanding of the scene.

From there, the project identifies court landmarks to estimate the geometry of the playing surface. Once the court is mapped, each player's foot position can be projected into a normalized mini-court coordinate space. This is an important step because it removes camera perspective effects and allows the system to reason about player movement as if it were happening on a standard tennis court.

The ball is treated similarly. Its path is interpolated over time so that short detection gaps do not break the trajectory. Once the trajectories are reconstructed, the project can estimate shot segments, ball speed, and the motion of the nearest opposing player.

Finally, the system merges all of this into a single annotated output: a rendered video with bounding boxes, keypoints, court overlays, mini-court mapping, and player stats. The project becomes a real-time storytelling tool for match analysis.

---

## What the project does

### 1. Detects players and the ball
The system leverages object detection models to identify tennis players and the ball from each frame. This process produces tracked bounding boxes and temporal object identities.

Key files:
- `main.py`
- `trackers/player_tracker.py`
- `trackers/ball_tracker.py`
- `yolo_inference.py`

### 2. Tracks objects across frames
Tracking is essential because a single frame is not enough to understand movement. The project tracks players and ball positions across consecutive frames and preserves identities over time.

This enables the system to reason about:
- player movement continuity
- ball trajectory over multiple frames
- shot segments and transitions
- motion between the moment a shot is hit and the response

### 3. Detects court structure using keypoints
A court line detection model estimates keypoints associated with the tennis court. These points allow the system to locate the field geometry and anchor a player or ball position to the actual court.

Important components:
- `court_line_detector/court_line_detector.py`
- `models/keypoints_model.pth`

### 4. Maps everything onto a mini-court
One of the most important ideas in this project is the mini-court mapping. Instead of analyzing a 2D video in its original perspective, the system converts real-world positions into a simplified court representation.

This makes it possible to:
- compare player positions consistently across frames
- understand movement relative to the court lines
- estimate proximity to the ball
- measure distance traveled by players and the ball
- visualize tactical and spatial behavior cleanly

This work is implemented in:
- `mini_court/mini_court.py`
- `utils/bbox_utils.py`

### 5. Estimates match-level metrics
Once trajectories are reconstructed, the system computes motion distances and approximates speed in physical units. It can estimate:
- ball travel distance between shot events
- ball shot speed
- opposing player speed during a response window
- shot counts by player
- average movement summaries

These metrics are then drawn onto the final output frames as player statistics.

This logic is in:
- `main.py`
- `utils/player_stats_drawer_utils.py`

### 6. Produces an annotated output video
The final component packages all of this into a rendered video. It overlays:
- player bounding boxes
- ball detections
- court keypoints
- mini-court reference
- player positions on the mini-court
- ball positions
- frame counters and stat panels

The output is saved in:
- `output_videos/`

---

## Project architecture

The repository is organized into a few core modules that each play a specific role in the tennis analysis pipeline.

```text
Tennis_Analysis_System/
├── main.py                          # Main orchestration script
├── yolo_inference.py                # YOLO inference entry point
├── README.md                       # Project overview and usage guide
├── models/                         # Trained detection and keypoint models
│   ├── best_1.pt
│   ├── best_1280.pt
│   ├── keypoints_model.pth
│   └── yolov8x.pt
├── trackers/                       # Player and ball tracking logic
│   ├── __init__.py
│   ├── ball_tracker.py
│   └── player_tracker.py
├── court_line_detector/            # Court geometry and keypoint detection
│   ├── __init__.py
│   └── court_line_detector.py
├── mini_court/                     # Mini-court projection and visualization
│   ├── __init__.py
│   └── mini_court.py
├── utils/                          # Geometry, video, and metric helper functions
│   ├── __init__.py
│   ├── bbox_utils.py
│   ├── conversions.py
│   ├── player_stats_drawer_utils.py
│   └── video_utils.py
├── constants/                     # Court measurements and calibration values
│   └── __init__.py
├── training/                      # Training notebooks and dataset references
├── input_videos/                  # Input match videos
├── output_videos/                 # Generated annotated outputs
├── runs/                          # YOLO prediction artefacts
├── stubs/                         # Saved detections for reuse
├── tracker_stubs/                 # Ball-tracking cached data
└── analysis/                      # Analysis notebooks and experiments
```

---

## Scientific and engineering approach

This project combines several ideas from computer vision and sports analytics:

### Object detection
The project uses YOLO-style detection to find players and objects within each frame. This is the foundation of the system and allows the model to identify relevant structures in the scene.

### Tracking and temporal continuity
A detection alone is not enough for tactical analysis. Tracking ensures that each player or the ball keeps a consistent identity across frames, which makes movement and event analysis possible.

### Geometry and court reconstruction
The project does not assume the camera is fixed or perfectly aligned. Instead, it estimates court geometry using detected line/keypoint information. This enables a more realistic conversion from image coordinates to court coordinates.

### Spatial normalization
The mini-court transformation is a major component. It makes the analysis interpretable by converting camera-space observations into court-space coordinates. This is especially helpful when comparing movement patterns and shot zones.

### Metric extraction
The system approximates spatial distances using court calibration values and converts pixel distances into meters. This allows the pipeline to estimate the speed and distance of the ball and players in physically meaningful units.

---

## How the main analysis flow works

The entry point is `main.py`, and the flow is roughly as follows:

1. Read the input video frame by frame.
2. Detect players and tennis ball objects.
3. Load or reuse stored detection data from stub files when available.
4. Interpolate ball positions to smooth gaps.
5. Detect court keypoints and identify court geometry.
6. Filter players that are valid for court-based analysis.
7. Create a mini-court and map player/ball positions into court coordinates.
8. Detect shot segments and estimate movement metrics.
9. Generate player stats such as shot counts and movement speeds.
10. Draw all overlays and save the final output video.

This is not just a toy pipeline; it is a complete analysis workflow designed for sports understanding.

---

## Important project characteristics

### Real-world constraints
This project is built around the challenges of real tennis footage:

- camera perspective distortion
- moving players and ball
- partial occlusions
- variable frame quality
- court geometry reconstruction from imperfect detections
- conversion from image pixels to real court distances

### Engineering decisions
The codebase contains practical decisions that matter in a production-style computer vision workflow:

- stub-based inference for faster reruns
- cached object detections for experimentation
- mini-court reconstruction from court landmarks
- distance conversions based on court dimensions
- frame-by-frame video output rendering

### Reproducibility
The project is designed to be rerun and refined. Data, models, and helper utilities are separated into modules so experiments can be improved without rewriting the whole pipeline.

---

## Models and training assets

This repository includes both detection and court-model assets:

- `yolov8x` for player detection
- `models/best_1.pt` for ball detection
- `models/keypoints_model.pth` for court line detection
- training notebooks in `training/`
- YOLO prediction outputs in `runs/`

The training directory contains notebooks and dataset references used during the model development process, which gives the repository a full development lifecycle narrative from experimentation to inference.

---

## Data and output

### Input data
The repository expects tennis video footage in `input_videos/`.

### Output data
The project writes processed videos to `output_videos/` and stores prediction artifacts in `runs/`.

Typical output includes:
- annotated player boxes
- ball boxes and labels
- court markers
- mini-court overlays
- player and ball location overlays
- summary stats on the output frames

---

## Usage

### Install dependencies
This project relies on tools such as OpenCV, Ultralytics, NumPy, and pandas.

```bash
conda activate yolo-projects
pip install -r requirements.txt
```

If `requirements.txt` is not present in the project root, install the relevant packages manually:

```bash
pip install ultralytics opencv-python numpy pandas matplotlib
```

### Run the analysis pipeline
```bash
python main.py
```

This runs the full end-to-end pipeline and outputs a processed video file into `output_videos/`.

### Run inference directly
```bash
python yolo_inference.py
```

---

## Current project status

This repository is an active sports analytics and computer vision project. It is not just a static example; it is a working pipeline with the following characteristics:

- object detection is in place
- player and ball tracking are integrated
- court geometry reconstruction is implemented
- mini-court conversion is in the pipeline
- metrics and performance summaries are generated
- video rendering is implemented

The project is in a strong research-and-development state, and it is positioned well for deeper tactical analysis and refinement.

---

## Key technical ideas worth highlighting

### Mini-court transformation
This is one of the most distinctive parts of the project. It translates the camera view into a canonical tennis court reference system, which makes the analysis much more meaningful than raw pixel tracking.

### Shot and movement analysis
The model estimates when ball movement indicates a shot, calculates distance covered between shot frames, and measures the motion of the opposing player in the same interval.

### Real-world interpretation
The project is not only about detection accuracy; it is about converting detection output into meaningful sports intelligence: which player was closest to the ball, how quickly the ball moved, how much distance the opponent covered, and where players were relative to the court.

---

## Future opportunities

There are several natural next steps for this project:

- improve motion smoothing and tracking robustness
- add stronger event detection for serves, returns, and rallies
- build a more complete player-to-team assignment system
- evaluate analytics on longer match sequences
- add richer tactical visualizations
- create dashboards or reports based on extracted statistics
- integrate more advanced court calibration workflows

---

## Final thought

This project is best understood as a system for turning video into understanding. A regular tennis video is only a sequence of frames unless a model can interpret the geometry, the motion, and the court context. This repository tries to do exactly that.

It is a story of perception, reconstruction, and insight: from raw footage to understandings of player movement, ball dynamics, and court behavior.

That is the core idea behind the project.

---

## License

This project is currently being developed for research, experimentation, and sports analytics learning. Licensing can be added and formalized as the project matures.

---

## Credits

Built as a sports analytics and computer vision project focused on real-time tennis understanding.
