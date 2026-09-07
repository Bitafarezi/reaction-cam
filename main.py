import cv2
import pyvirtualcam
from gesture_detector import GestureDetector
from meme_fetcher import MemeFetcher
from camera_overlay import apply_overlay

def main():
    detector = GestureDetector()
    fetcher = MemeFetcher()

    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    last_gesture = None

    print("Program started! Select 'Virtual Camera' in Google Meet video settings.")

    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
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
                frame = apply_overlay(frame, fetcher.current_meme)
            else:
                last_gesture = None

            # 4. Output frame to virtual camera
            cam.send(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cam.sleep_until_next_frame()

    cap.release()

if __name__ == "__main__":
    main()