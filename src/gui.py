import cv2

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow

from generated_files.MainWindow import Ui_MainWindow
from plot import PlotCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.detectVideo.update_frame.connect(self.update_cameras)
        self.pixmap = QPixmap()
        self.ui.detectVideo.setScaledContents(True)
        self.ui.disabledVideo.setScaledContents(True)
        self.ui.enabledVideo.setScaledContents(True)
        self.energyWidget: PlotCanvas = self.ui.energyWidget
        self.bandwidthWidget: PlotCanvas = self.ui.bandwidthWidget
        self.peakMemoryWidget: PlotCanvas = self.ui.peakMemoryWidget
        self.update_plots()
        self.show()

    def update_plots(self):
        self.energyWidget.axes.plot([1,2,3], [1,2,3], 'r')
        self.bandwidthWidget.axes.plot([1,2,3], [1,2,3], 'r')
        self.peakMemoryWidget.axes.plot([1,2,3], [1,2,3], 'r')
        self.energyWidget.draw()
        self.bandwidthWidget.draw()
        self.peakMemoryWidget.draw()

    def update_cameras(self, pixmap: QPixmap):
        self.pixmap = pixmap
        disabledVideoSize = self.ui.disabledVideo.size()
        enabledVideoSize = self.ui.enabledVideo.size()
        detectVideoSize = self.ui.detectVideo.size()
        self.ui.disabledVideo.setPixmap(pixmap.scaled(
            disabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.enabledVideo.setPixmap(pixmap.scaled(
            enabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.detectVideo.setPixmap(pixmap.scaled(
            detectVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
