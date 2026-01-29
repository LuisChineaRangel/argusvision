import numpy as np
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class HandResult:
    landmarks: list
    label: str
    gesture: Optional[str]
    is_moving: bool
    fingers_count: int

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


@dataclass
class EngineViewState:
    frame: np.ndarray
    fps: float
    fingers: int
    hands: int
    gestures: list[str]
