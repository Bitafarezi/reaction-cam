# Reaction Cam 🎭📸

**Reaction Cam** is a fully offline, real-time Python application designed for platforms like Google Meet, Zoom, and MS Teams via a virtual webcam. It automatically detects specific custom hand gestures and overlays corresponding local memes directly over your face using computer vision and landmark analysis.

---

## ✨ Features

- **100% Offline & Instant:** Loads images directly from a local RAM cache rather than fetching from remote APIs, eliminating network latency and rate limits.
- **Custom Gesture Detection:** Uses custom 2D geometric landmark analysis over MediaPipe to recognize complex, multi-hand poses (such as the T-pose timeout, prayer hands, or pointing gestures).
- **Face Matching & Alignment:** Uses MediaPipe FaceMesh to accurately track face bounding boxes and position transparent overlays seamlessly over the user's face.
- **Transparency Support:** Supports PNG, JPEG, WebP, and AVIF image formats with full alpha-channel transparency.
- **Mirrored Virtual Webcam:** Integrates with `pyvirtualcam` and automatically mirrors overlays so they align perfectly in mirrored video preview feeds (e.g., Google Meet).

---

## 📂 Project Structure

```text
reaction-cam/
├── assets/
│   └── memes/      
├── gesture_detector.py       # Custom MediaPipe hand landmark detection logic
├── meme_fetcher.py           # Local file reader with image caching & transparency support
├── camera_overlay.py         # FaceMesh tracking & image overlay calculation
├── main.py                   # Main loop & virtual camera streaming
├── requirements.txt          # Python dependencies
└── README.md
```

## 🛠️ Trigger Gestures & Meme Mapping

| Gesture Name | Physical Hand Pose | Action / Overlay Image |
| :--- | :--- | :--- |
| **`Timeout`** | Form a **T-shape** using both hands (one horizontal on top of one vertical). | Overlays `Timeout.png` |
| **`Exhasted`** | Press both palms together vertically in front of your face/chest (Prayer pose). | Overlays `Exhasted.png` |
| **`Stop_Cross`** | Hold one open palm facing towards the camera (`Open_Palm`). | Overlays `Stop_Cross.png` |
| **`Refusal`** | Point your index finger vertically upwards (`Pointing_Up`). | Overlays `Refusal.png` |

---

## 🚀 Installation & Setup

### 1. Prerequisites
- **Python:** `3.11` recommended.
- **Virtual Camera Loopback Driver:**
  - **macOS:** Install [OBS Studio](https://obsproject.com/) (includes OBS Virtual Camera) or `macam`.
  - **Linux:** Install `v4l2loopback` (`sudo apt install v4l2loopback-dkms`).
  - **Windows:** Install OBS Studio or Unity Capture.


### 2. Clone & Install Dependencies

```bash
# Clone the repository
git clone [https://github.com/your-username/reaction-cam.git](https://github.com/your-username/reaction-cam.git)
cd reaction-cam
```

```bash
# Create and activate a virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

```bash
# Install required packages
pip install -r requirements.txt
```


### 3. MediaPipe Model File
Ensure you have downloaded the MediaPipe Gesture Recognizer model task file (gesture_recognizer.task) into the root directory of the project.


## 🎮 How to Run

### 1.Make sure your local memes are placed inside assets/memes/:
Timeout.png
Refusal.png
Stop_Cross.png
Exhasted.png

### 2.Run the main script:
```python
python3.11 main.py
```

### 3.Open your video meeting app (Google Meet, Zoom, Teams, OBS).
### 4.Select pyvirtualcam or OBS Virtual Camera as your camera source in the meeting settings.
### 5.Perform any of the target hand gestures in front of your camera to trigger the corresponding meme overlay!
