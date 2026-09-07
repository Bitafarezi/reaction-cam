import cv2
import pyvirtualcam
from gesture_detector import GestureDetector
from meme_fetcher import MemeFetcher
from camera_overlay import apply_overlay

def main():
    detector = GestureDetector()
    fetcher = MemeFetcher()

    cap = cv2.VideoCapture(0)
    
    # Set explicit camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    last_gesture = None

    print(f"Program started! Camera resolution: {width}x{height}")
    print("Select 'OBS Virtual Camera' in Google Meet video settings.")

    with pyvirtualcam.Camera(width=width, height=height, fps=30, fmt=pyvirtualcam.PixelFormat.RGB) as cam:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            # Mirror frame horizontally for natural view
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 1. Detect hand gesture
            gesture = detector.detect(rgb_frame)

            if gesture:
                # 2. Fetch new meme asynchronously if gesture changed
                if gesture != last_gesture:
                    last_gesture = gesture
                    fetcher.fetch_async(gesture)
                
                # 3. Apply meme overlay
                if fetcher.current_meme is not None:
                    rgb_frame = apply_overlay(rgb_frame, fetcher.current_meme)
            else:
                last_gesture = None

            # 4. Output frame to virtual camera
            cam.send(rgb_frame)
            cam.sleep_until_next_frame()

    cap.release()

if __name__ == "__main__":
    main()