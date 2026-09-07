import mediapipe as mp
import math
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
            num_hands=2
        )
        self.recognizer = GestureRecognizer.create_from_options(options)

    def _distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def detect(self, rgb_frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        frame_timestamp_ms = int(time.time() * 1000)
        
        result = self.recognizer.recognize_for_video(mp_image, frame_timestamp_ms)

        if not result.hand_landmarks or len(result.hand_landmarks) == 0:
            return None

        if len(result.hand_landmarks) == 2:
            hand1, hand2 = result.hand_landmarks[0], result.hand_landmarks[1]
            wrist1, wrist2 = hand1[0], hand2[0]
            index1, index2 = hand1[8], hand2[8]

            wrist_dist = self._distance(wrist1, wrist2)
            index_dist = self._distance(index1, index2)

            if wrist_dist < 0.25 and index_dist < 0.25:
                return "Exhasted"

            y_diff1 = abs(wrist1.y - index1.y)
            y_diff2 = abs(wrist2.y - index2.y)
            if (y_diff1 < 0.20 and y_diff2 > 0.15) or (y_diff2 < 0.20 and y_diff1 > 0.15):
                if wrist_dist < 0.5:
                    return "Timeout"

        top_gesture = result.gestures[0][0] if result.gestures else None
        if top_gesture and top_gesture.score > 0.4:
            name = top_gesture.category_name
            
            if name in ["Pointing_Up", "Victory"]:
                return "Refusal"
            elif name == "Open_Palm":
                return "Stop_Cross"

        return None