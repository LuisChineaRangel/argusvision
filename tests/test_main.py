import pytest
from unittest.mock import MagicMock, patch
import numpy as np
import time
from argusvision.main import VisionWorker, ArgusVisionApp
from argusvision.engine.models import EngineViewState

def test_vision_worker_initialization_failure():
    worker = VisionWorker()

    with patch('argusvision.main.HandRenderer', side_effect=Exception("Initialization failed")):
        error_spy = MagicMock()
        worker.error_occurred.connect(error_spy)

        worker.run()
        assert error_spy.called

@patch('cv2.VideoCapture')
@patch('argusvision.main.HandRenderer')
def test_vision_worker_camera_error(mock_renderer, mock_cap):
    """Verify error when camera is not available."""
    inst = mock_cap.return_value
    inst.isOpened.return_value = False

    worker = VisionWorker()
    error_spy = MagicMock()
    worker.error_occurred.connect(error_spy)

    worker.run()

    assert error_spy.called
    args, _ = error_spy.call_args
    assert args[0] == "Camera not available"

@patch('argusvision.main.QGuiApplication')
@patch('argusvision.main.QQmlApplicationEngine')
def test_app_lifecycle(mock_qml, mock_qapp):
    """Test the basic orchestration of the QML application."""
    with patch('argusvision.main.ViewBridge') as mock_bridge_cls, \
         patch('argusvision.main.VideoImageProvider') as mock_vip_cls:

        app = ArgusVisionApp()
        assert app.engine is not None
        assert app.worker is not None
        assert app.bridge is not None

        # Verify UI update
        state = EngineViewState(np.zeros((10,10,3)), 30.0, 5, 1, ["Right: Peace Sign"])
        app.update_ui(state)

        # Use mock handles to satisfy the linter
        mock_bridge_cls.return_value.update_state.assert_called_with(state)
        mock_vip_cls.return_value.update_frame.assert_called()

def test_app_cleanup():
    """Verify that cleanup stops threads and workers."""
    with patch('argusvision.main.QGuiApplication'), \
         patch('argusvision.main.QQmlApplicationEngine'), \
         patch('argusvision.main.ViewBridge'), \
         patch('argusvision.main.VideoImageProvider'):

        app = ArgusVisionApp()
        mock_thread = MagicMock()
        app.worker_thread = mock_thread
        mock_worker = MagicMock()
        app.worker = mock_worker

        app.cleanup()

        mock_worker.stop.assert_called_once()
        mock_thread.quit.assert_called_once()
        mock_thread.wait.assert_called_once()

def test_vision_worker_successful_iteration():
    """Simulate a successful iteration of the processing loop."""
    worker = VisionWorker()

    with patch('cv2.VideoCapture') as mock_cap, \
         patch('argusvision.main.HandRenderer') as mock_renderer:

        # Simulate valid frame
        cap_inst = mock_cap.return_value
        cap_inst.isOpened.return_value = True
        cap_inst.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

        # Simulate renderer result
        mock_state = EngineViewState(
            frame=np.zeros((480, 640, 3)),
            fps=30.0,
            fingers=5,
            hands=1,
            gestures=["Right: Peace Sign"]
        )
        mock_renderer.return_value.render_frame.return_value = mock_state

        state_spy = MagicMock()
        worker.state_updated.connect(state_spy)

        # Run once and stop the loop
        def stop_worker(*args, **kwargs):
            worker.running = False
            return (True, np.zeros((480, 640, 3), dtype=np.uint8))

        cap_inst.read.side_effect = stop_worker

        worker.run()

        # Verify that the correct state was emitted
        assert state_spy.called
        state = state_spy.call_args[0][0]
        assert state.fingers == 5
        assert state.hands == 1
        assert "Right: Peace Sign" in state.gestures

def test_app_run_integration():
    """Test the run method of the main application."""
    with patch('argusvision.main.QGuiApplication'), \
         patch('argusvision.main.QQmlApplicationEngine'), \
         patch('argusvision.main.ViewBridge'), \
         patch('argusvision.main.VideoImageProvider'):

        app = ArgusVisionApp()
        app.worker_thread.start = MagicMock()
        app.app.exec.return_value = 0

        with patch.object(app, 'cleanup') as mock_cleanup:
            exit_code = app.run()
            assert exit_code == 0
            assert mock_cleanup.called
            assert app.worker_thread.start.called

def test_main_entry_point():
    """Test that the main() entry point initializes the app."""
    with patch('argusvision.main.ArgusVisionApp') as mock_app_cls:
        from argusvision.main import main
        with patch('sys.exit'):
            main()
            assert mock_app_cls.return_value.run.called
