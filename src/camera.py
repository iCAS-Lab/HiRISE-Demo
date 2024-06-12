import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtCore import QSize, QTimer, Signal, Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QImage, QPixmap
from hirise import HiRISE

################################################################################
YOLO_MODEL_PATH = './src/models/face_det.pt'


class Camera(QLabel):

    update_frame = Signal(tuple)
    update_stats = Signal(dict)

    def __init__(self, parent):
        QLabel.__init__(self)
        self.video_size = QSize(self.width(), self.height())
        self.setup_camera()
        self.hirise_call = HiRISE()

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
        self.timer.start(1)

    def set_tab(self, new_tab: str):
        self.tab = new_tab

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        # print(f'Reading Frame: {time.time()}')
        res, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        # Perform detection
        detect, baseline, hirise = None, None, None
        detect, baseline, hirise, stats = self.hirise_call.detect(
            res, frame, self.tab)
        # Check that we have valid results
        if detect is not None and baseline is not None and hirise is not None:
            detect_image = QImage(detect, detect.shape[1], detect.shape[0],
                                  detect.strides[0], QImage.Format.Format_RGB888)
            detect_pm = QPixmap.fromImage(detect_image)
            baseline_image = QImage(baseline, baseline.shape[1], baseline.shape[0],
                                    baseline.strides[0], QImage.Format.Format_RGB888)
            baseline_pm = QPixmap.fromImage(baseline_image)
            hirise_image = QImage(hirise, hirise.shape[1], hirise.shape[0],
                                  hirise.strides[0], QImage.Format.Format_RGB888)
            hirise_pm = QPixmap.fromImage(hirise_image)
            # print(f'Sending Update: {time.time()}')
            self.update_frame.emit((detect_pm, baseline_pm, hirise_pm))
            self.update_stats.emit(stats)
        # else:
        #     # Use default image otherwise
        #     frame = cv2.resize(frame, (96, 96))
        #     image = QImage(frame, frame.shape[1], frame.shape[0],
        #                    frame.strides[0], QImage.Format.Format_RGB888)
        #     pixmap = QPixmap.fromImage(image)
        #     detect_pm, baseline_pm, hirise_pm = (pixmap, pixmap, pixmap)
        # Emit Signals to update GUI
