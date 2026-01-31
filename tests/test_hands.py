import numpy as np
from dataclasses import dataclass
from argusvision.logic import (
    GeometryUtils,
    HandGeometry,
    HandMetrics,
    PeaceSign,
    ThumbUp,
    ThumbDown,
    HandGestureValidator,
)


@dataclass
class MockLandmark:
    x: float
    y: float


def create_mock_landmarks():
    # Initialize 21 landmarks (default mediapipe hands)
    return [MockLandmark(0.5, 0.5) for _ in range(21)]


def test_is_finger_extended():
    landmarks = create_mock_landmarks()
    # Wrist at (0.5, 0.5)
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)
    # Index TIP at (0.5, 0.0) - far from wrist
    landmarks[HandMetrics.INDEX] = MockLandmark(0.5, 0.0)
    # Index PIP at (0.5, 0.5) - closer to wrist
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.5, 0.5)

    pose = HandGeometry(landmarks)
    assert pose.is_finger_extended(HandMetrics.INDEX) is True


def test_is_finger_not_extended():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)

    landmarks[HandMetrics.INDEX] = MockLandmark(0.5, 0.6)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.5, 0.5)
    # TIP closer to wrist than PIP

    pose = HandGeometry(landmarks)
    assert pose.is_finger_extended(HandMetrics.INDEX) is False


def test_peace_sign_matches():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)

    # Extend Index and Middle
    landmarks[HandMetrics.INDEX] = MockLandmark(0.4, 0.0)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.4, 0.5)

    landmarks[HandMetrics.MIDDLE] = MockLandmark(0.6, 0.0)
    landmarks[HandMetrics.MIDDLE - 2] = MockLandmark(0.6, 0.5)

    # Keep others closed (TIP close to WRIST)
    for tip in [HandMetrics.THUMB, HandMetrics.RING, HandMetrics.PINKY]:
        landmarks[tip] = MockLandmark(0.5, 0.9)
        landmarks[tip - 2] = MockLandmark(0.5, 0.8)

    # Note: Thumb logic is special, let's adjust it for PeaceSign to not be extended
    landmarks[HandMetrics.THUMB - 3] = MockLandmark(0.4, 0.8)
    landmarks[HandMetrics.PINKY - 3] = MockLandmark(0.6, 0.8)
    landmarks[HandMetrics.THUMB] = MockLandmark(
        0.5, 0.8
    )  # Between mcp and pinky (closed)

    gesture = PeaceSign()
    assert gesture.matches(landmarks) is True


def test_peace_sign_no_match():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)
    # Extend Index and Middle
    landmarks[HandMetrics.INDEX] = MockLandmark(0.4, 0.0)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.4, 0.5)
    landmarks[HandMetrics.MIDDLE] = MockLandmark(0.6, 0.0)
    landmarks[HandMetrics.MIDDLE - 2] = MockLandmark(0.6, 0.5)
    # ALSO extend Pinky (should fail matches)
    landmarks[HandMetrics.PINKY] = MockLandmark(0.8, 0.0)
    landmarks[HandMetrics.PINKY - 2] = MockLandmark(0.8, 0.5)

    gesture = PeaceSign()
    assert gesture.matches(landmarks) is False


def test_thumb_up_matches():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)

    # Thumb extended and TIP.y < TIP-2.y
    landmarks[HandMetrics.THUMB] = MockLandmark(0.2, 0.5)
    landmarks[HandMetrics.THUMB - 2] = MockLandmark(0.3, 0.6)
    landmarks[HandMetrics.THUMB - 3] = MockLandmark(0.4, 0.7)
    landmarks[HandMetrics.PINKY - 3] = MockLandmark(0.6, 0.7)

    # Others closed
    for tip in [
        HandMetrics.INDEX,
        HandMetrics.MIDDLE,
        HandMetrics.RING,
        HandMetrics.PINKY,
    ]:
        landmarks[tip] = MockLandmark(0.5, 0.9)
        landmarks[tip - 2] = MockLandmark(0.5, 0.8)

    gesture = ThumbUp()
    assert gesture.matches(landmarks) is True


def test_thumb_up_no_match():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)
    # Extend Thumb
    landmarks[HandMetrics.THUMB] = MockLandmark(0.2, 0.5)
    landmarks[HandMetrics.THUMB - 2] = MockLandmark(0.3, 0.6)
    landmarks[HandMetrics.THUMB - 3] = MockLandmark(0.4, 0.7)
    landmarks[HandMetrics.PINKY - 3] = MockLandmark(0.6, 0.7)
    # ALSO extend Index
    landmarks[HandMetrics.INDEX] = MockLandmark(0.5, 0.0)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.5, 0.5)

    gesture = ThumbUp()
    assert gesture.matches(landmarks) is False


def test_thumb_down_matches():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 0.0)

    # Thumb extended and TIP.y > TIP-2.y
    landmarks[HandMetrics.THUMB] = MockLandmark(0.2, 0.5)
    landmarks[HandMetrics.THUMB - 2] = MockLandmark(0.3, 0.4)
    landmarks[HandMetrics.THUMB - 3] = MockLandmark(0.4, 0.3)
    landmarks[HandMetrics.PINKY - 3] = MockLandmark(0.6, 0.3)

    # Others closed
    for tip in [
        HandMetrics.INDEX,
        HandMetrics.MIDDLE,
        HandMetrics.RING,
        HandMetrics.PINKY,
    ]:
        landmarks[tip] = MockLandmark(0.5, 0.1)
        landmarks[tip - 2] = MockLandmark(0.5, 0.2)

    gesture = ThumbDown()
    assert gesture.matches(landmarks) is True


def test_thumb_down_no_match():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 0.0)
    # Extend Thumb
    landmarks[HandMetrics.THUMB] = MockLandmark(0.2, 0.5)
    landmarks[HandMetrics.THUMB - 2] = MockLandmark(0.3, 0.4)
    landmarks[HandMetrics.THUMB - 3] = MockLandmark(0.4, 0.3)
    landmarks[HandMetrics.PINKY - 3] = MockLandmark(0.6, 0.3)
    # ALSO extend Index
    landmarks[HandMetrics.INDEX] = MockLandmark(0.5, 0.9)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.5, 0.5)

    gesture = ThumbDown()
    assert gesture.matches(landmarks) is False


def test_get_extended_count():
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0.5, 1.0)
    # Index extended
    landmarks[HandMetrics.INDEX] = MockLandmark(0.4, 0.0)
    landmarks[HandMetrics.INDEX - 2] = MockLandmark(0.4, 0.5)

    pose = HandGeometry(landmarks)

    assert pose.get_extended_count() == 1


def test_hand_gesture_validator():
    landmarks = create_mock_landmarks()
    # None should match
    assert HandGestureValidator.identify(landmarks) is None


def test_hand_geometry_internal_distance():
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])
    # distance should be 5
    assert GeometryUtils.get_distance(p1, p2) == 5.0


def test_hand_geometry_is_extended_logic():
    # Test that it correctly identifies extension based on distance to wrist
    landmarks = create_mock_landmarks()
    landmarks[HandMetrics.WRIST] = MockLandmark(0, 0)

    # TIP (Id 8) further than PIP (Id 6)
    landmarks[8] = MockLandmark(0, 10)
    landmarks[6] = MockLandmark(0, 5)
    pose = HandGeometry(landmarks)
    assert pose.is_finger_extended(8) is True

    # TIP (Id 8) closer than PIP (Id 6)
    landmarks[8] = MockLandmark(0, 4)
    pose = HandGeometry(landmarks)
    assert pose.is_finger_extended(8) is False
