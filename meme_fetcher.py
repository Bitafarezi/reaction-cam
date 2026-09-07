import requests
import cv2
import numpy as np
import threading

KEYWORDS = {
    "Open_Palm": "Surprised!",
    "Closed_Fist": "Angry!",
    "Thumb_Up": "Like!",
    "Thumb_Down": "Dislike!",
    "Victory": "Peace!",
    "Pointing_Up": "Aha!",
    "ILoveYou": "Love!"
}

class MemeFetcher:
    def __init__(self):
        self.cache = {}
        self.current_meme = None
        self.is_downloading = False

    def _generate_fallback_image(self, text):
        img = np.zeros((240, 240, 3), dtype=np.uint8)
        img[:] = (60, 20, 40)
        cv2.rectangle(img, (5, 5), (235, 235), (0, 255, 255), 2)
        
        cv2.putText(img, text, (20, 130), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
        
        img = cv2.flip(img, 1)
        return img

    def _download_worker(self, gesture, text):
        try:
            # Alternate API endpoint
            url = f"https://api.popcat.xyz/meme"
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                image_url = response.json().get("image")
                img_resp = requests.get(image_url, timeout=3)
                img_array = np.asarray(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is not None:
                    self.cache[gesture] = img
                    self.current_meme = img
                    return
        except Exception:
            pass

        # If network fails or times out, immediately use generated offline image
        fallback = self._generate_fallback_image(text)
        self.cache[gesture] = fallback
        self.current_meme = fallback
        self.is_downloading = False

    def fetch_async(self, gesture):
        text = KEYWORDS.get(gesture, gesture)
        
        if gesture in self.cache:
            self.current_meme = self.cache[gesture]
            return self.current_meme

        if not self.is_downloading:
            self.is_downloading = True
            threading.Thread(target=self._download_worker, args=(gesture, text), daemon=True).start()

        return self.current_meme