import numpy as np
from argusvision.engine.models import HandResult, EngineViewState

def test_hand_result_getitem():
    res = HandResult(
        landmarks=[],
        label="Left",
        gesture="Peace Sign",
        is_moving=False,
        fingers_count=2
    )
    assert res["label"] == "Left"
    assert res["gesture"] == "Peace Sign"
    assert res["fingers_count"] == 2
    assert res["is_moving"] is False

def test_engine_view_state_creation():
    frame = np.zeros((100, 100, 3))
    state = EngineViewState(
        frame=frame,
        fps=30.0,
        fingers=5,
        hands=1,
        gestures=["None"]
    )
    assert state.fps == 30.0
    assert state.fingers == 5
    assert np.array_equal(state.frame, frame)
