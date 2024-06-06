"""_summary_
https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
"""

import cv2
import numpy as np
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
        self.ui.detectVideo.update_plots.connect(self.update_plots)
        self.pixmap = QPixmap()
        self.ui.detectVideo.setScaledContents(True)
        self.ui.disabledVideo.setScaledContents(True)
        self.ui.enabledVideo.setScaledContents(True)
        self.energyTab: PlotCanvas = self.ui.energyTab
        self.energyTab.axes.set_title('Energy')
        self.bandwidthTab: PlotCanvas = self.ui.bandwidthTab
        self.bandwidthTab.axes.set_title('Bandwidth')
        self.peakMemoryTab: PlotCanvas = self.ui.peakMemoryTab
        self.peakMemoryTab.axes.set_title('Peak Memory')
        self.current_plot_data = (0, 0, 0)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.plot_ref = None
        self.xdata = np.arange(50)
        self.ydata = np.random.randint(10, size=50)
        self.current_tab: PlotCanvas = self.ui.tabWidget.currentWidget()
        self.update_plots((0,0,0))
        self.show()
    
    def tab_changed(self):
        self.current_tab: PlotCanvas = self.ui.tabWidget.currentWidget()
        self.current_tab.axes.clear()
        self.plot_ref = None
        print(self.current_tab)
        self.update_plots(self.current_plot_data)

    def update_plots(self, plot_data: tuple):
        self.current_plot_data = plot_data
        peak_memory, bandwidth, energy = plot_data
        print(self.current_tab)
        self.ydata = np.concatenate((self.ydata[1:], np.random.randint(10, size=1)))
        if self.plot_ref is None:
            plot_refs = self.current_tab.axes.plot(self.xdata, self.ydata, 'r')
            self.plot_ref = plot_refs[0]
        else:
            self.plot_ref.set_ydata(self.ydata)
        self.current_tab.draw()
        # self.energyTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.bandwidthTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.peakMemoryTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.energyTab.draw()
        # self.bandwidthTab.draw()
        # self.peakMemoryTab.draw()

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
