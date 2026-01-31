import cv2

class AppConfig:
    TITLE = "ArgusVision"
    FPS_TARGET = 30
    FRAME_DELAY = 33  # ms
    # Performance
    PROCESS_WIDTH = 480

class Theme:
    # Color palette (RGB)
    PRIMARY = (0, 255, 204)     # Neon Cyan
    SECONDARY = (255, 82, 82)   # Coral Red
    SUCCESS = (76, 175, 80)     # Green
    ACCENT = (33, 150, 243)     # Blue

    PANEL_BG = (26, 26, 26)     # Dark Gray
    SECTION_BG = (30, 30, 30)   # Surface
    TEXT_MAIN = (255, 255, 255)
    TEXT_DIM = (136, 136, 136)

    FONT = cv2.FONT_HERSHEY_SIMPLEX
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    QT_FONT_FAMILY = "Segoe UI"
