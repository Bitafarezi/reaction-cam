import urllib.request
import json
import cv2
import numpy as np
import threading
import random


GESTURE_MEMES = {
    "Open_Palm": ["surprisedtalkingfaces", "shockedmemes", "memes"],
    "Closed_Fist": "maddudes",
    "Thumb_Up": ["wholesomememes", "ThumbsUp"],
    "Thumb_Down": ["funny", "disappointed"],
    "Victory": "wholesomememes",
    "Pointing_Up": "mindblown"
}

class MemeFetcher:
    def __init__(self):
        self.cache = {}
        self.current_meme = None
        self.is_downloading = False

    def _download_worker(self, gesture):
        subreddits = GESTURE_MEMES.get(gesture, "memes")
        sub = random.choice(subreddits) if isinstance(subreddits, list) else subreddits
        
        url = f"https://meme-api.com/gimme/{sub}"

        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )

        try:
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                img_url = data.get("url")

                if img_url:
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(img_req, timeout=4) as img_response:
                        img_array = np.asarray(bytearray(img_response.read()), dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                        if img is not None:
                            img = cv2.resize(img, (300, 300))
                            img = cv2.flip(img, 1) 
                            self.current_meme = img
                            self.is_downloading = False
                            return
        except Exception as e:
            print(f"Error downloading meme for {gesture}: {e}")

        self.is_downloading = False

    def fetch_async(self, gesture):
        if not self.is_downloading:
            self.is_downloading = True
            threading.Thread(target=self._download_worker, args=(gesture,), daemon=True).start()

        return self.current_meme