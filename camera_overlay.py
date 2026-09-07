import cv2
import numpy as np

def apply_overlay_on_face(frame, meme_img, face_landmarks):
    if meme_img is None or face_landmarks is None:
        return frame

    h, w, _ = frame.shape

    x_coords = [lm.x * w for lm in face_landmarks.landmark]
    y_coords = [lm.y * h for lm in face_landmarks.landmark]

    min_x, max_x = int(min(x_coords)), int(max(x_coords))
    min_y, max_y = int(min(y_coords)), int(max(y_coords))

    face_width = max_x - min_x
    face_height = max_y - min_y

    margin = int(face_width * 0.3)
    new_w = max(1, face_width + (margin * 2))
    new_h = max(1, face_height + (margin * 2))

    resized_meme = cv2.resize(meme_img, (new_w, new_h))

    top_y = max(0, min_y - margin)
    left_x = max(0, min_x - margin)
    bottom_y = min(h, top_y + new_h)
    right_x = min(w, left_x + new_w)

    overlay_h = bottom_y - top_y
    overlay_w = right_x - left_x

    if overlay_h <= 0 or overlay_w <= 0:
        return frame

    resized_meme = resized_meme[:overlay_h, :overlay_w]

    if resized_meme.shape[2] == 4:
        alpha = resized_meme[:, :, 3] / 255.0
        alpha_inv = 1.0 - alpha

        for c in range(0, 3):
            frame[top_y:bottom_y, left_x:right_x, c] = (
                alpha * resized_meme[:, :, c] +
                alpha_inv * frame[top_y:bottom_y, left_x:right_x, c]
            )
    else:
        frame[top_y:bottom_y, left_x:right_x] = resized_meme[:, :, :3]

    return frame