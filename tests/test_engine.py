import os
import pytest
import numpy as np
from argusvision.engine import HandEngine
from argusvision.logic.gestures import HandMetrics


def test_hand_engine_initialization():
    # Only test if model file exists
    if not os.path.exists("assets/mp_models/hand_landmarker.task"):
        pytest.skip("Model file not found")

    try:
        engine = HandEngine(use_gpu=False)
        assert engine.detector is not None
        assert engine._prev_positions == {}
    except Exception as e:
        pytest.fail(f"HandEngine failed to initialize: {e}")

def test_resolve_label():
    # We need a dummy object that has handedness[0].category_name
    class DummyHandedness:
        def __init__(self, category_name):
            self.category_name = category_name

    engine = HandEngine.__new__(HandEngine) # Skip init

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
