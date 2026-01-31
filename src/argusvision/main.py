import sys
import cv2
import os
import time
import PySide6
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QThread, Signal, QObject, QUrl

from .engine import HandRenderer, EngineViewState
from .views.bridge import ViewBridge, VideoImageProvider
from .logic import AppConfig

pyside_dir = os.path.dirname(PySide6.__file__)
os.environ['QT_PLUGIN_PATH'] = os.path.join(pyside_dir, "plugins")
os.environ['QML2_IMPORT_PATH'] = os.path.join(pyside_dir, "qml")

current_dir = os.path.dirname(__file__)
os.environ['QT_QUICK_CONTROLS_CONF'] = os.path.join(current_dir, "views", "qtquickcontrols2.conf")

if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(pyside_dir)


class VisionWorker(QObject):
    state_updated = Signal(EngineViewState)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.renderer = None
        self.cap = None

    def run(self):
        try:
            self.renderer = HandRenderer()
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            self.error_occurred.emit(f"Initialization failed: {e}")
            return

        if not self.cap or not self.cap.isOpened():
            self.error_occurred.emit("Camera not available")
            return

        while self.running:
            start_time = time.time()
            success, frame = self.cap.read()
            if not success:
                continue

            try:
                state = self.renderer.render_frame(frame)
                if state:
                    self.state_updated.emit(state)
            except Exception as e:
                self.error_occurred.emit(str(e))
                break

            # Control frame rate to save CPU
            elapsed = (time.time() - start_time) * 1000
            delay = max(1, AppConfig.FRAME_DELAY - elapsed)
            time.sleep(delay / 1000.0)

        if self.cap:
            self.cap.release()

    def stop(self):
        self.running = False


class ArgusVisionApp(QObject):
    def __init__(self):
        super().__init__()

        self.app = QGuiApplication.instance() or QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        views_path = os.path.join(os.path.dirname(__file__), "views")
        self.engine.addImportPath(views_path)

        self.bridge = ViewBridge()
        self.image_provider = VideoImageProvider()

        self.engine.addImageProvider("video", self.image_provider)
        self.engine.setInitialProperties({"view_bridge": self.bridge})

        qml_file = os.path.join(os.path.dirname(__file__), "views", "Main.qml")
        self.engine.load(QUrl.fromLocalFile(qml_file))

        if not self.engine.rootObjects():
            sys.exit(-1)

        self.worker_thread = QThread(self)
        self.worker = VisionWorker()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.state_updated.connect(self.update_ui)
        self.worker.error_occurred.connect(print)

    def update_ui(self, state):
        self.bridge.update_state(state)
        self.image_provider.update_frame(state.frame)

    def run(self):
        print(f"Starting {AppConfig.TITLE} interface (Qt Quick)...")
        self.worker_thread.start()

        exit_code = self.app.exec()
        self.cleanup()
        return exit_code

    def cleanup(self):
        self.worker.stop()
        self.worker_thread.quit()
        self.worker_thread.wait()

def main():
    app = ArgusVisionApp()
    try:
        exit_code = app.run()
        sys.exit(exit_code)
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
