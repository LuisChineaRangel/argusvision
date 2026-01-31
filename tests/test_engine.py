import pytest
import numpy as np
from argusvision.engine import HandEngine
from unittest.mock import MagicMock, patch
from argusvision.logic.gestures import HandMetrics


def test_hand_engine_initialization_failure():
    with patch("argusvision.engine.hand_engine.HandLandmarker.create_from_options") as mock_create:
        mock_create.side_effect = Exception("Initialization error")
        with pytest.raises(Exception, match="Initialization error"):
            HandEngine(use_gpu=False)


def test_hand_engine_process_frame_no_hands():
    with patch("argusvision.engine.hand_engine.HandLandmarker.create_from_options"):
        engine = HandEngine(use_gpu=False)
        mock_result = MagicMock()
        mock_result.hand_landmarks = []
        engine.detector.detect_for_video = MagicMock(return_value=mock_result)

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        hands = engine.process_frame(frame, timestamp_ms=0)
        assert hands == []


def test_hand_engine_process_frame_with_hands():
    with patch("argusvision.engine.hand_engine.HandLandmarker.create_from_options"):
        engine = HandEngine(use_gpu=False)

        # Mocking a landmark result
        mock_lm = MagicMock()
        mock_lm.x, mock_lm.y, mock_lm.z = 0.5, 0.5, 0.0

        mock_result = MagicMock()
        mock_result.hand_landmarks = [[mock_lm] * 21]

        mock_handedness = MagicMock()
        mock_handedness.category_name = "Left"
        mock_result.handedness = [[mock_handedness]]

        engine.detector.detect_for_video = MagicMock(return_value=mock_result)

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        hands = engine.process_frame(frame, timestamp_ms=0)

        assert len(hands) == 1
        assert hands[0].label == "Right"  # Mirrored
        assert hands[0].is_moving is False


def test_resolve_label():
    # We need a dummy object that has handedness[0].category_name
    class DummyHandedness:
        def __init__(self, category_name):
            self.category_name = category_name

    engine = HandEngine.__new__(HandEngine)  # Skip init

    assert engine._resolve_label([DummyHandedness("Left")]) == "Right"
    assert engine._resolve_label([DummyHandedness("Right")]) == "Left"


def test_detect_movement():
    engine = HandEngine.__new__(HandEngine)
    engine._prev_positions = {}
    engine._movement_history = {}

    p1 = np.array([0.5, 0.5])
    p2 = np.array([0.5, 0.5 + HandMetrics.MOVEMENT_THRESHOLD * 2])

    # First frame, no movement
    assert engine._detect_movement(p1, 0) is False
    assert engine._prev_positions[0] is p1

    # Significant movement
    assert engine._detect_movement(p2, 0) is True
    assert engine._movement_history[0] == 8

    # Tiny movement (should still be True because of history persistence)
    p3 = np.array([0.5, 0.5 + HandMetrics.MOVEMENT_THRESHOLD * 2.01])
    assert engine._detect_movement(p3, 0) is True
    assert engine._movement_history[0] == 7
