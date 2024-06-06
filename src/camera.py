import cv2
from PySide6.QtCore import QSize, QTimer, Signal, Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QImage, QPixmap


class Camera(QLabel):

    update_frame = Signal(QPixmap)
    update_plots = Signal(tuple)

    def __init__(self, parent):
        QLabel.__init__(self)
        self.video_size = QSize(self.width(),self.height())
        self.setup_camera()

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,
                         self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,
                         self.video_size.height())
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(
            'M', 'J', 'P', 'G'))  # depends on fourcc available camera
        self.capture.set(cv2.CAP_PROP_FPS, 30)

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        res, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.update_frame.emit(pixmap)
        self.update_plots.emit((1,1,1))

