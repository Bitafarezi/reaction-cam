import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class GestureDetector:
    def __init__(self, model_path="gesture_recognizer.task"):
        
        # Load the downloaded AI gesture recognition model
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            num_hands=1
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def detect(self, rgb_frame):
        # Convert OpenCV frame to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Recognize gesture using the AI model
        recognition_result = self.recognizer.recognize(mp_image)

        # Check if a valid gesture was recognized
        if recognition_result.gestures and len(recognition_result.gestures) > 0:
            top_gesture = recognition_result.gestures[0][0]
            
            # Return category name if confidence score is above 50%
            if top_gesture.score > 0.5 and top_gesture.category_name != "None":
                return top_gesture.category_name

        return None