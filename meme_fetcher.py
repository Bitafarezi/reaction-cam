import urllib.request
import json
import cv2
import numpy as np
import threading
import os

KEYWORDS = {
    "Open_Palm": "surprised meme",
    "Closed_Fist": "angry meme",
    "Thumb_Up": "thumbs up meme",
    "Thumb_Down": "disappointed meme",
    "Victory": "happy meme",
    "Pointing_Up": "mind blown meme"
}

class MemeFetcher:
    def __init__(self):
        self.cache = {}
        self.current_meme = None
        self.is_downloading = False

    def _generate_placeholder(self, gesture):
        """تولید تصویر موقت با کیفیت بالا هنگام کندی اینترنت"""
        img = np.zeros((280, 280, 3), dtype=np.uint8)
        img[:] = (50, 20, 60)
        cv2.rectangle(img, (10, 10), (270, 270), (0, 255, 200), 3)
        cv2.putText(img, "Loading Meme...", (35, 145), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return cv2.flip(img, 1)

    def _download_worker(self, gesture):
        query = KEYWORDS.get(gesture, "meme")
        # استفاده از سرویس CATAAS (Cats as a Service) یا منبع مستقیم عکس با ترافیک آزاد
        url = f"https://cataas.com/cat/says/{urllib.parse.quote(query)}?width=300&height=300"

        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )

        try:
            # دانلود مستقیم فریم تصویر از طریق urllib با Time-out کوتاه
            with urllib.request.urlopen(req, timeout=3) as response:
                img_data = response.read()
                img_array = np.asarray(bytearray(img_data), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is not None:
                    img = cv2.resize(img, (280, 280))
                    img = cv2.flip(img, 1) # تنظیم آینه‌ای برای گوگل میت
                    self.cache[gesture] = img
                    self.current_meme = img
                    self.is_downloading = False
                    return
        except Exception as e:
            print(f"Fallback active for {gesture}: {e}")

        # استفاده از placeholder گرافیکی در صورت عدم پاسخ‌گویی شبکه
        placeholder = self._generate_placeholder(gesture)
        self.cache[gesture] = placeholder
        self.current_meme = placeholder
        self.is_downloading = False

    def fetch_async(self, gesture):
        if gesture in self.cache:
            self.current_meme = self.cache[gesture]
            return self.current_meme

        if not self.is_downloading:
            self.is_downloading = True
            self.current_meme = self._generate_placeholder(gesture)
            threading.Thread(target=self._download_worker, args=(gesture,), daemon=True).start()

        return self.current_meme