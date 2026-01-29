import numpy as np

class GeometryUtils:
    @staticmethod
    def get_distance(p1: np.ndarray, p2: np.ndarray) -> float:
        return float(np.linalg.norm(p1 - p2))
