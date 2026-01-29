import cv2

class AppConfig:
    TITLE = "ArgusVision"
    FPS_TARGET = 30
    FRAME_DELAY = 33  # ms
    # Performance
    PROCESS_WIDTH = 480

class Theme:
    # Color palette (RGB)
    PRIMARY = (255, 87, 34)     # Material Deep Orange
    SECONDARY = (231, 76, 60)   # Material Red
    SUCCESS = (76, 175, 80)     # Material Green
    ACCENT = (33, 150, 243)     # Material Blue

    PANEL_BG = (18, 18, 18)     # Material Dark Background
    SECTION_BG = (30, 30, 30)   # Material Surface
    TEXT_MAIN = (255, 255, 255)
    TEXT_DIM = (176, 176, 176)

    FONT = cv2.FONT_HERSHEY_SIMPLEX
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
