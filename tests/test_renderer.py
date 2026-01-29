import numpy as np
from dataclasses import dataclass
from argusvision.engine import Renderer

@dataclass
class MockLM:
    x: float
    y: float

def test_renderer_clamp():
    assert Renderer._clamp(10, 0, 100) == 10
    assert Renderer._clamp(-5, 0, 100) == 0
    assert Renderer._clamp(150, 0, 100) == 100

def test_get_pixel_array():
    renderer = Renderer()
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
    renderer = Renderer()
    from argusvision.logic import Theme
    # Check if colors are reversed (RGB to BGR)
    assert renderer.c_primary == Theme.PRIMARY[::-1]
