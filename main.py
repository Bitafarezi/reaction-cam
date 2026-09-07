import cv2
import pyvirtualcam
import mediapipe as mp
from gesture_detector import GestureDetector
from meme_fetcher import MemeFetcher
from camera_overlay import apply_overlay_on_face

def main():
    detector = GestureDetector()
    fetcher = MemeFetcher()

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=False,
        min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    last_gesture = None

    print(f"Program started! Camera resolution: {width}x{height}")

    with pyvirtualcam.Camera(width=width, height=height, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            display_frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            
            gesture = detector.detect(rgb_frame)

            face_results = face_mesh.process(rgb_frame)
            face_landmarks = face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None

            if gesture:
                if gesture != last_gesture:
                    last_gesture = gesture
                    fetcher.fetch_async(gesture)
                
                if fetcher.current_meme is not None and face_landmarks:
                    display_frame = apply_overlay_on_face(display_frame, fetcher.current_meme, face_landmarks)
            else:
                last_gesture = None

            cam.send(display_frame)
            cam.sleep_until_next_frame()

    cap.release()

if __name__ == "__main__":
    main()