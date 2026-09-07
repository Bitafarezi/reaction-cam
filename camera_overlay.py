import cv2

def apply_overlay(background, overlay, size=(240, 240), pos_offset=(280, 40)):
    """Resizes and overlays the meme image onto the webcam frame."""
    if overlay is None:
        return background

    h, w, _ = background.shape
    overlay_resized = cv2.resize(overlay, size)
    oh, ow, _ = overlay_resized.shape

    x = max(0, min(w - pos_offset[0], w - ow))
    y = max(0, min(pos_offset[1], h - oh))

    background[y:y+oh, x:x+ow] = overlay_resized
    return background