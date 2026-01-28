import cv2
import numpy as np
from logic import Theme, HandMetrics

# Hand skeleton paths grouped by functional segments for vectorized drawing
HAND_PATHS = [
    [0, 1, 2, 3, 4],              # Thumb
    [5, 6, 7, 8],                 # Index
    [9, 10, 11, 12],              # Middle
    [13, 14, 15, 16],             # Ring
    [17, 18, 19, 20],             # Pinky
    [0, 5, 9, 13, 17, 0]          # Palm Bridge
]

class Renderer:
    def __init__(self):
        self.font = Theme.FONT
        # Pre-convert colors to BGR for OpenCV
        self.c_primary = Theme.PRIMARY[::-1]
        self.c_success = Theme.SUCCESS[::-1]
        self.c_secondary = Theme.SECONDARY[::-1]
        self.c_panel = Theme.PANEL_BG[::-1]
        self.c_text = Theme.TEXT_MAIN[::-1]

    @staticmethod
    def _clamp(value: int, min_v: int, max_v: int) -> int:
        return max(min_v, min(value, max_v))

    def _get_pixel_array(self, landmarks, width: int, height: int) -> np.ndarray:
        coords = np.array([(lm.x * width, lm.y * height) for lm in landmarks])
        return np.clip(coords, [0, 0], [width - 1, height - 1]).astype(int)

    def draw_skeleton_base(self, frame: np.ndarray, points: np.ndarray, paths: list, color=None):
        color = color or self.c_primary
        for path in paths:
            pts = points[path].reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], False, (0, 0, 0), 4, cv2.LINE_AA)  # Shadow
            cv2.polylines(frame, [pts], False, color, 2, cv2.LINE_AA)

    def draw_points(self, frame: np.ndarray, points: np.ndarray, color=None):
        color = color or self.c_success
        for p in points:
            center = tuple(p)
            cv2.circle(frame, center, 5, color, -1, cv2.LINE_AA)
            cv2.circle(frame, center, 6, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_label(self, frame: np.ndarray, text: str, anchor: tuple[int, int], color=None):
        h, w, _ = frame.shape
        x, y = anchor
        color = color or self.c_primary

        (tw, th), _ = cv2.getTextSize(text, self.font, 0.65, 2)
        pad_x, pad_y = 10, 8

        # Boundaries check
        x = self._clamp(x, 0, w - tw - pad_x * 2)
        y = self._clamp(y - 10, th + pad_y, h)

        rect_start = (x, y - th - pad_y)
        rect_end = (x + tw + pad_x * 2, y + pad_y)

        # Shadow
        cv2.rectangle(frame, (rect_start[0] + 2, rect_start[1] + 2), (rect_end[0] + 2, rect_end[1] + 2), (0, 0, 0), -1)
        # Background
        cv2.rectangle(frame, rect_start, rect_end, self.c_panel, -1)
        # Border
        cv2.rectangle(frame, rect_start, rect_end, color, 2, cv2.LINE_AA)
        # Text
        cv2.putText(frame, text, (x + pad_x, y), self.font, 0.65, self.c_text, 2, cv2.LINE_AA)


class HandRenderer(Renderer):
    def draw_hand(self, frame: np.ndarray, hand_data):
        h, w, _ = frame.shape

        pixel_points = self._get_pixel_array(hand_data.landmarks, w, h)
        wrist_px = tuple(pixel_points[HandMetrics.WRIST])

        self.draw_skeleton_base(frame, pixel_points, HAND_PATHS)
        self.draw_points(frame, pixel_points)

        text = f"{hand_data.label}: {hand_data.gesture}" if hand_data.gesture else hand_data.label
        self.draw_label(frame, text, wrist_px)

        if hand_data.is_moving:
            self._draw_motion_status(frame, wrist_px)

    def _draw_motion_status(self, frame: np.ndarray, anchor: tuple[int, int]):
        x, y = anchor
        cv2.putText(frame, "MOVING", (x + 10, y + 20), self.font, 0.5, self.c_secondary, 1, cv2.LINE_AA)
