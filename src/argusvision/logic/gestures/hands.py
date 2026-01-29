import numpy as np
from abc import ABC, abstractmethod
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmark
from ..utils import GeometryUtils

class HandMetrics:
    WRIST = HandLandmark.WRIST

    THUMB = HandLandmark.THUMB_TIP
    INDEX = HandLandmark.INDEX_FINGER_TIP
    MIDDLE = HandLandmark.MIDDLE_FINGER_TIP
    RING = HandLandmark.RING_FINGER_TIP
    PINKY = HandLandmark.PINKY_TIP
    TIPS = [THUMB, INDEX, MIDDLE, RING, PINKY]

    # Sensitivity settings
    MOVEMENT_THRESHOLD = 0.025
    GESTURE_PRECISION = 0.05

class HandGeometry:
    def __init__(self, landmarks: list) -> None:
        self.landmarks = landmarks

    def is_finger_extended(self, tip: int) -> bool:
        if tip == HandMetrics.THUMB:
            pinky_mcp = self.landmarks[HandMetrics.PINKY - 3]
            thumb_mcp = self.landmarks[HandMetrics.THUMB - 3]
            thumb_tip = self.landmarks[HandMetrics.THUMB]

            thumb_mcp = np.array([thumb_mcp.x, thumb_mcp.y])
            pinky_mcp = np.array([pinky_mcp.x, pinky_mcp.y])
            thumb_tip = np.array([thumb_tip.x, thumb_tip.y])

            base_dist = GeometryUtils.get_distance(thumb_mcp, pinky_mcp)
            tip_dist = GeometryUtils.get_distance(thumb_tip, pinky_mcp)

            return tip_dist > base_dist * (1 - HandMetrics.GESTURE_PRECISION)

        # Other fingers
        wrist = self.landmarks[HandMetrics.WRIST]
        wrist = np.array([wrist.x, wrist.y])
        tip_pos = np.array([self.landmarks[tip].x, self.landmarks[tip].y])
        pip = np.array([self.landmarks[tip - 2].x, self.landmarks[tip - 2].y])
        tip_dist = GeometryUtils.get_distance(tip_pos, wrist)
        pip_dist = GeometryUtils.get_distance(pip, wrist)

        return tip_dist > pip_dist * (1 + HandMetrics.GESTURE_PRECISION)

    def get_extended_count(self) -> int:
        count = 0
        for tip in HandMetrics.TIPS:
            if self.is_finger_extended(tip):
                count += 1
        return count

class HandGesture(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def matches(self, landmarks: list) -> bool:
        pass

class PeaceSign(HandGesture):
    @property
    def name(self) -> str: return "Peace Sign"

    def matches(self, landmarks: list) -> bool:
        pose = HandGeometry(landmarks)

        if not pose.is_finger_extended(HandMetrics.INDEX) or not pose.is_finger_extended(HandMetrics.MIDDLE):
            return False

        for tip in [HandMetrics.THUMB, HandMetrics.RING, HandMetrics.PINKY]:
            if pose.is_finger_extended(tip):
                return False

        return True

class ThumbUp(HandGesture):
    @property
    def name(self) -> str: return "Good Job"

    def matches(self, landmarks: list) -> bool:
        pose = HandGeometry(landmarks)

        if not pose.is_finger_extended(HandMetrics.THUMB):
            return False

        for tip in [HandMetrics.INDEX, HandMetrics.MIDDLE, HandMetrics.RING, HandMetrics.PINKY]:
            if pose.is_finger_extended(tip):
                return False

        return landmarks[HandMetrics.THUMB].y < landmarks[HandMetrics.THUMB - 2].y

class ThumbDown(HandGesture):
    @property
    def name(self) -> str: return "Disapproval"

    def matches(self, landmarks: list) -> bool:
        pose = HandGeometry(landmarks)

        if not pose.is_finger_extended(HandMetrics.THUMB):
            return False

        for tip in [HandMetrics.INDEX, HandMetrics.MIDDLE, HandMetrics.RING, HandMetrics.PINKY]:
            if pose.is_finger_extended(tip):
                return False

        return landmarks[HandMetrics.THUMB].y > landmarks[HandMetrics.THUMB - 2].y

GESTURES: list[HandGesture] = [
    PeaceSign(),
    ThumbUp(),
    ThumbDown()
]

class HandGestureValidator:
    @staticmethod
    def identify(landmarks: list) -> str | None:
        for gesture in GESTURES:
            if gesture.matches(landmarks):
                return gesture.name
        return None
