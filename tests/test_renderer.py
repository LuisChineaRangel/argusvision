import numpy as np
from dataclasses import dataclass
from argusvision.logic import Theme
from argusvision.engine import Renderer, EngineViewState


@dataclass
class MockLM:
    x: float
    y: float

class MockRenderer(Renderer):
    def _analyze_and_draw(self, frame: np.ndarray):
        return EngineViewState(frame, 0, 0, 0, [])

def test_renderer_clamp():
    assert Renderer._clamp(10, 0, 100) == 10
    assert Renderer._clamp(-5, 0, 100) == 0
    assert Renderer._clamp(150, 0, 100) == 100

def test_get_pixel_array():
    renderer = MockRenderer()
    landmarks = [
        MockLM(0.1, 0.2),
        MockLM(0.5, 0.5),
        MockLM(1.1, -0.1) # Out of bounds
    ]
    width, height = 100, 200
    pixels = renderer._get_pixel_array(landmarks, width, height)

    expected = np.array([
        [10, 40],
        [50, 100],
        [99, 0] # Clamped
    ])
    assert np.array_equal(pixels, expected)

def test_renderer_init():
    renderer = MockRenderer()
    # Check if colors are reversed (RGB to BGR)
    assert renderer.c_primary == Theme.PRIMARY[::-1]

def test_render_frame_workflow():
    renderer = MockRenderer()
    # Create a 100x100 black frame with a white pixel at (10, 10)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[10, 10] = [255, 255, 255]

    state = renderer.render_frame(frame)

    # Test flipping: In original, (10, 10) is white.
    # OpenCv Horizontal flip: index (row, col) becomes (row, width - 1 - col)
    # (10, 10) -> (10, 100 - 1 - 10) = (10, 89)
    assert np.all(state.frame[10, 89] == 255)
    assert state.fps >= 0

def test_draw_methods_smoke():
    """Smoke test to ensure CV2 drawing methods don't crash."""
    renderer = MockRenderer()
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    points = np.array([[100, 100], [200, 200]], dtype=int)

    # Should run without error
    renderer.draw_skeleton_base(frame, points, [[0, 1]])
    renderer.draw_points(frame, points)
    renderer.draw_label(frame, "Test", (100, 100))

    assert frame.any() # Should have drawn something
