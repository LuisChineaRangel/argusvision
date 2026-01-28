import sys
import cv2
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal, QObject
from engine import HandRenderer as Renderer
from engine import EngineViewState, HandEngine
from ui.dashboard import ArgusVisionWindow
from logic import AppConfig


class VisionWorker(QObject):
    state_updated = Signal(EngineViewState)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.tracker = None
        self.canvas = None
        self.cap = None

    def run(self):
        prev_time = 0

        # Initialize resources only when the worker_thread starts
        try:
            self.tracker = HandEngine(use_gpu=False)
            self.canvas = Renderer()
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            self.error_occurred.emit(f"Initialization failed: {e}")
            return

        if not self.cap or not self.cap.isOpened():
            self.error_occurred.emit("Camera not available")
            return

        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            try:
                # Pre-processing
                frame = cv2.flip(frame, 1)
                h, w = frame.shape[:2]

                # Resizing for engine performance
                scale = AppConfig.PROCESS_WIDTH / w
                process_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

                timestamp_ms = int(time.time() * 1000)
                processed_hands = self.tracker.process_frame(process_frame, timestamp_ms)

                # Logic & Drawing
                detected_gestures = []
                total_fingers = sum(h.fingers_count for h in processed_hands)

                for hand_data in processed_hands:
                    if hand_data.gesture:
                        detected_gestures.append(f"{hand_data.label}: {hand_data.gesture}")
                    self.canvas.draw_hand(frame, hand_data)

                # FPS Calculation
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time else 0
                prev_time = curr_time

                state = EngineViewState(
                    frame=frame,
                    fps=fps,
                    fingers=total_fingers,
                    hands=len(processed_hands),
                    gestures=detected_gestures
                )
                self.state_updated.emit(state)

            except Exception as e:
                self.error_occurred.emit(str(e))
                break

        if self.cap:
            self.cap.release()

    def stop(self):
        self.running = False


class ArgusVisionApp(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = ArgusVisionWindow()
        self.window.exit_requested.connect(self.window.close)

        # Threading setup
        self.worker_thread = QThread(self)
        self.worker = VisionWorker()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.state_updated.connect(self.update_ui)
        self.worker.error_occurred.connect(print)

    def update_ui(self, state):
        self.window.update(state)

    def run(self):
        print(f"Starting {AppConfig.TITLE} interface...")
        self.worker_thread.start()
        self.window.showMaximized()

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
