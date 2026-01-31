import cv2
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider

class VideoImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self.current_frame = QImage()

    def requestImage(self, id, size, requested_size):
        if self.current_frame.isNull():
            img = QImage(640, 480, QImage.Format.Format_RGB32)
            img.fill(0)
            return img
        return self.current_frame

    def update_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        self.current_frame = QImage(rgb_frame.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()

class ViewBridge(QObject):
    frameUpdated = Signal()

    def __init__(self):
        super().__init__()
        self._fps = 0
        self._fingers = 0
        self._hands = 0
        self._gestures = []

    @Property(int, notify=frameUpdated)
    def fps(self): return self._fps

    @Property(int, notify=frameUpdated)
    def fingers(self): return self._fingers

    @Property(int, notify=frameUpdated)
    def hands(self): return self._hands

    @Property(list, notify=frameUpdated)
    def gestures(self): return self._gestures

    @Slot(object)
    def update_state(self, state):
        self._fps = state.fps
        self._fingers = state.fingers
        self._hands = state.hands
        self._gestures = state.gestures
        self.frameUpdated.emit()
