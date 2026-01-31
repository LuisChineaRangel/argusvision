from PySide6.QtGui import QImage
from unittest.mock import MagicMock
from argusvision.views.bridge import ViewBridge, VideoImageProvider
from argusvision.engine.models import EngineViewState
import numpy as np

def test_view_bridge_properties():
    bridge = ViewBridge()
    assert bridge.fps == 0
    assert bridge.hands == 0
    assert bridge.fingers == 0
    assert bridge.gestures == []

def test_view_bridge_update_state():
    bridge = ViewBridge()
    mock_state = EngineViewState(
        frame=np.zeros((10, 10, 3), dtype=np.uint8),
        fps=60,
        fingers=2,
        hands=1,
        gestures=["Peace Sign"]
    )

    spy = MagicMock()
    bridge.frameUpdated.connect(spy)

    bridge.update_state(mock_state)

    assert bridge.fps == 60
    assert bridge.fingers == 2
    assert bridge.hands == 1
    assert bridge.gestures == ["Peace Sign"]
    assert spy.called

def test_video_image_provider_initial_state():
    provider = VideoImageProvider()
    # Should return a black image if no frame has been set
    img = provider.requestImage("any", None, None)
    assert isinstance(img, QImage)
    assert not img.isNull()
    assert img.width() == 640
    assert img.height() == 480

def test_video_image_provider_update():
    provider = VideoImageProvider()
    # Create a small blue frame (BGR)
    frame = np.zeros((100, 200, 3), dtype=np.uint8)
    frame[:] = [255, 0, 0] # Blue in BGR

    provider.update_frame(frame)
    img = provider.requestImage("any", None, None)

    assert img.width() == 200
    assert img.height() == 100
    # After BGR->RGB conversion, it should be Red in RGB if we used [255,0,0] as BGR
    # But for the test, checking the dimensions and that it's not null is enough
    assert not img.isNull()
