from __future__ import annotations
import numpy as np
from typing import Any

from mediapipe import Image, ImageFormat
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    HandLandmarkerOptions,
    HandLandmarker,
    RunningMode,
)

from logic import HandMetrics, HandGestureValidator, HandGeometry
from engine import HandResult


class HandEngine:
    def __init__(self, use_gpu: bool = False) -> None:
        try:
            self._initialize_detector(use_gpu)
        except Exception as e:
            if use_gpu:
                print(f"GPU initialization failed, falling back to CPU: {e}")
                self._initialize_detector(use_gpu=False)
            else:
                raise e

    def _initialize_detector(self, use_gpu: bool) -> None:
        delegate = BaseOptions.Delegate.GPU if use_gpu else BaseOptions.Delegate.CPU
        base_options = BaseOptions("assets/mp_models/hand_landmarker.task", delegate)
        options = HandLandmarkerOptions(base_options, RunningMode.VIDEO, 2, 0.5)

        self.detector = HandLandmarker.create_from_options(options)

        # Tracking state
        self._prev_positions: dict[int, np.ndarray] = {}
        self._movement_history: dict[int, int] = {}  # Frames remaining for "moving" state

    def process_frame(self, frame: np.ndarray, timestamp_ms: int) -> list[HandResult]:
        mp_image = Image(ImageFormat.SRGB, frame)
        results = self.detector.detect_for_video(mp_image, timestamp_ms)
        return self._process_results(results)

    def _process_results(self, results: Any) -> list[HandResult]:
        if not results.hand_landmarks:
            self._prev_positions.clear()
            self._movement_history.clear()
            return []

        hands: list[HandResult] = []

        for idx, landmarks in enumerate(results.hand_landmarks):
            curr_pos_array = np.array([landmarks[0].x, landmarks[0].y])
            label = self._resolve_label(results.handedness[idx])

            # Persist movement state to avoid flickering
            is_moving = self._detect_movement(curr_pos_array, idx)

            gesture = HandGestureValidator.identify(landmarks)
            finger_count = HandGeometry(landmarks).get_extended_count()
            hands.append(HandResult(landmarks, label, gesture, is_moving, finger_count))

        return hands

    def _resolve_label(self, handedness: list) -> str:
        detected = handedness[0].category_name
        return "Right" if detected == "Left" else "Left"

    def _detect_movement(self, current_pos: np.ndarray, idx: int) -> bool:
        prev_pos = self._prev_positions.get(idx)
        self._prev_positions[idx] = current_pos

        if prev_pos is None:
            return False

        dist = np.linalg.norm(current_pos - prev_pos)

        if dist > HandMetrics.MOVEMENT_THRESHOLD:
            self._movement_history[idx] = 8  # Stay "moving" for N frames
        else:
            self._movement_history[idx] = max(0, self._movement_history.get(idx, 0) - 1)

        return self._movement_history[idx] > 0
