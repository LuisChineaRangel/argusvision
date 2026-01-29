import numpy as np
import pytest
from argusvision.logic.utils import GeometryUtils

def test_get_distance():
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])
    assert GeometryUtils.get_distance(p1, p2) == 5.0

    p1 = np.array([1, 1])
    p2 = np.array([1, 1])
    assert GeometryUtils.get_distance(p1, p2) == 0.0

    p1 = np.array([-1, -1])
    p2 = np.array([2, 3])
    # dist = sqrt((2 - -1)^2 + (3 - -1)^2) = sqrt(3^2 + 4^2) = 5
    assert GeometryUtils.get_distance(p1, p2) == 5.0
