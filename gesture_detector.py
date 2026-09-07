import mediapipe as mp
import time

class GestureDetector:
    def __init__(self, model_path="gesture_recognizer.task"):
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=1
        )
        self.recognizer = GestureRecognizer.create_from_options(options)

    def detect(self, rgb_frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        frame_timestamp_ms = int(time.time() * 1000)
        
        recognition_result = self.recognizer.recognize_for_video(mp_image, frame_timestamp_ms)

        if recognition_result.gestures and len(recognition_result.gestures) > 0:
            top_gesture = recognition_result.gestures[0][0]
    
            if top_gesture.score > 0.65 and top_gesture.category_name != "None":
                return top_gesture.category_name

        return None