import cv2
import os

ALLOWED_MEMES = ["Timeout", "Refusal", "Stop_Cross", "Exhasted"]

class MemeFetcher:
    def __init__(self, memes_dir="assets/memes"):
        self.memes_dir = memes_dir
        self.cache = {}
        self.current_meme = None

    def fetch_async(self, gesture):
        if gesture not in ALLOWED_MEMES:
            self.current_meme = None
            return None

        if gesture in self.cache:
            self.current_meme = self.cache[gesture]
            return self.current_meme

        for ext in [".png", ".jpg", ".jpeg", ".webp", ".avif"]:
            file_path = os.path.join(self.memes_dir, f"{gesture}{ext}")
            if os.path.exists(file_path):
                img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    img = cv2.flip(img, 1)
                    self.cache[gesture] = img
                    self.current_meme = img
                    return self.current_meme

        self.current_meme = None
        return None