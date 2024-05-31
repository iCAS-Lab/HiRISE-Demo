from PySide6.QtCore import *
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication, QGridLayout
from PySide6.QtGui import *
import cv2
import sys
import time


class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.video_size = QSize(1920, 1080)
        self.setup_ui()
        self.setup_camera()

    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)

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
        self.capture.set(cv2.CAP_PROP_FPS, 60)

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(1)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        res, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec())