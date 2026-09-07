import requests
import cv2
import numpy as np
import threading

# Mapping MediaPipe gestures to online meme search keywords
KEYWORDS = {
    "Open_Palm": "surprised",
    "Closed_Fist": "angry",
    "Thumb_Up": "thumbsup",
    "Thumb_Down": "disappointed",
    "Victory": "celebration",
    "Pointing_Up": "mind blown",
    "ILoveYou": "heart"
}

class MemeFetcher:
    def __init__(self):
        self.cache = {}
        self.current_meme = None
        self.is_downloading = False

    def _download_worker(self, keyword):
        try:
            # Fetch a random meme from the online Meme API
            url = f"https://meme-api.com/gimme/{keyword}"
            response = requests.get(url, timeout=3).json()
            image_url = response.get("url")

            if image_url:
                # Download image data and decode with OpenCV
                img_resp = requests.get(image_url, timeout=3)
                img_array = np.asarray(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is not None:
                    self.cache[keyword] = img
                    self.current_meme = img
        except Exception as e:
            print("Error downloading meme:", e)
        finally:
            self.is_downloading = False

    def fetch_async(self, gesture):
        keyword = KEYWORDS.get(gesture, "meme")
        
        # Use cached image if already downloaded
        if keyword in self.cache:
            self.current_meme = self.cache[keyword]
            return self.current_meme

        # Start asynchronous download if not currently fetching
        if not self.is_downloading:
            self.is_downloading = True
            threading.Thread(target=self._download_worker, args=(keyword,), daemon=True).start()

        return self.current_meme