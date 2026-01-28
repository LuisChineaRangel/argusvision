import cv2
import numpy as np
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QImage, QPixmap, QFont, QColor
from logic import Theme
from engine import EngineViewState

class BaseDashboardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._add_shadow()

    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)

    def _get_base_style(self, object_name: str) -> str:
        return f"""
        QFrame#{object_name} {{
            background-color: rgb{Theme.SECTION_BG};
            border-radius: 12px;
            padding: 15px;
            margin: 5px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        """

class StatsWidget(BaseDashboardFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statsWidget")
        self.setStyleSheet(self._get_base_style("statsWidget"))
        self._init_ui(title)

    def _init_ui(self, title: str):
        app_layout = QVBoxLayout(self)
        app_layout.setSpacing(5)

        self.title_label = QLabel(title.upper())
        self.title_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color: rgb{Theme.TEXT_DIM}; letter-spacing: 1px;")

        self.value_label = QLabel("--")
        self.value_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: rgb{Theme.TEXT_MAIN};")

        app_layout.addWidget(self.title_label)
        app_layout.addWidget(self.value_label)

    def set_value(self, value, color = None):
        self.value_label.setText(str(value))
        if color:
            self.value_label.setStyleSheet(f"color: rgb{color};")

class GestureListWidget(BaseDashboardFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("gestureWidget")
        self.setStyleSheet(self._get_base_style("gestureWidget"))
        self.gesture_labels: list[QLabel] = []
        self._init_ui()

    def _init_ui(self):
        self.app_layout = QVBoxLayout(self)
        self.app_layout.setSpacing(10)

        self.title_label = QLabel("DETECTED GESTURES")
        self.title_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color: rgb{Theme.TEXT_DIM}; letter-spacing: 1px;")

        self.app_layout.addWidget(self.title_label)
        self.app_layout.addStretch()

    def update_gestures(self, gestures: list[str]):
        # Update or create labels
        for i, gesture in enumerate(gestures):
            if i >= len(self.gesture_labels):
                label = QLabel()
                label.setFont(QFont("Segoe UI", 10))
                label.setStyleSheet(f"color: rgb{Theme.PRIMARY};")
                # Insert before the stretch
                self.app_layout.insertWidget(self.app_layout.count() - 1, label)
                self.gesture_labels.append(label)

            self.gesture_labels[i].setText(f"• {gesture}")
            self.gesture_labels[i].show()

        # Hide unused labels
        for label in self.gesture_labels[len(gestures):]:
            label.hide()


class ArgusVisionWindow(QMainWindow):
    """Main application window using a dark-themed modern dashboard."""
    exit_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArgusVision - Tracking Dashboard")
        self.setMinimumSize(1100, 800)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: rgb(18, 18, 18); }}
            QLabel {{ color: white; }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_app_layout = QHBoxLayout(central_widget)
        main_app_layout.setSpacing(0)
        main_app_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Video Display Area
        self.video_canvas = QLabel()
        self.video_canvas.setScaledContents(True)
        self.video_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_canvas.setStyleSheet("background-color: black; border-right: 1px solid rgba(255, 255, 255, 0.05);")
        main_app_layout.addWidget(self.video_canvas, stretch=5)

        # 2. Control Panel
        self.sidebar = self._setup_sidebar()
        main_app_layout.addWidget(self.sidebar, stretch=1)

    def _setup_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(340)
        sidebar.setStyleSheet(f"background-color: rgb{Theme.PANEL_BG}; border-left: 1px solid rgba(255, 255, 255, 0.1);")

        app_layout = QVBoxLayout(sidebar)
        app_layout.setSpacing(25)
        app_layout.setContentsMargins(25, 40, 25, 40)

        header = self._create_header()
        app_layout.addWidget(header)

        self.fps_widget = StatsWidget("System Performance")
        self.fingers_widget = StatsWidget("Active Fingers")
        self.hands_widget = StatsWidget("Detected Hands")
        self.gesture_widget = GestureListWidget()

        for w in [self.fps_widget, self.fingers_widget, self.hands_widget, self.gesture_widget]:
            app_layout.addWidget(w)

        app_layout.addStretch()

        self.exit_btn = self._create_exit_button()
        app_layout.addWidget(self.exit_btn)

        return sidebar

    def _create_header(self) -> QWidget:
        container = QWidget()
        app_layout = QVBoxLayout(container)
        app_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel("ArgusVision")
        title.setFont(QFont("Segoe UI Black", 24))
        title.setStyleSheet(f"color: rgb{Theme.PRIMARY}; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Tracking System")
        subtitle.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        subtitle.setStyleSheet(f"color: rgb{Theme.TEXT_DIM}; letter-spacing: 4px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_layout.addWidget(title)
        app_layout.addWidget(subtitle)
        return container

    def _create_exit_button(self) -> QPushButton:
        btn = QPushButton("TERMINATE SESSION")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: rgb{Theme.SECONDARY};
                border: 2px solid rgb{Theme.SECONDARY};
                border-radius: 10px;
                padding: 16px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ background-color: rgb{Theme.SECONDARY}; color: white; }}
            QPushButton:pressed {{ background-color: rgb(180, 50, 40); }}
        """)
        btn.clicked.connect(self.exit_requested.emit)
        return btn

    def update(self, state: EngineViewState):
        self._set_frame(state.frame)
        self._set_metrics(state)

    def _set_frame(self, frame: np.ndarray):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        qt_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()
        self.video_canvas.setPixmap(QPixmap.fromImage(qt_img))

    def _set_metrics(self, state: EngineViewState):
        fps_color = Theme.SUCCESS if state.fps > 25 else Theme.SECONDARY
        self.fps_widget.set_value(f"{int(state.fps)} FPS", fps_color)
        self.fingers_widget.set_value(state.fingers, Theme.ACCENT)
        self.hands_widget.set_value(state.hands, Theme.PRIMARY)
        self.gesture_widget.update_gestures(state.gestures)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.exit_requested.emit()
