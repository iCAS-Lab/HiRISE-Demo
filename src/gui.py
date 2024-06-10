"""_summary_
https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
"""

import numpy as np
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel

from generated_files.MainWindow import Ui_MainWindow
from plot import PlotCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        # Init GUI
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.make_summary_ui()

        # Connect signals to slots
        self.ui.detectVideo.update_frame.connect(self.update_cameras)
        self.ui.detectVideo.update_stats.connect(self.update_tab)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)

        # Temp pixmap
        self.pixmap = QPixmap()

        # Temporary data
        self.current_plot_data = (0, 0, 0)
        self.xdata = np.arange(50)
        self.baseline_data = np.random.randint(10, size=50)
        self.hirise_data = np.random.randint(10, size=50)

        # Scale contents to GUI, set False to preserve images quality
        self.ui.detectVideo.setScaledContents(True)
        self.ui.disabledVideo.setScaledContents(True)
        self.ui.enabledVideo.setScaledContents(True)

        # Setup Tabs
        self.energyTab: PlotCanvas = self.ui.energyTab
        self.bandwidthTab: PlotCanvas = self.ui.bandwidthTab
        self.peakMemoryTab: PlotCanvas = self.ui.peakMemoryTab
        self.current_tab: PlotCanvas = self.ui.tabWidget.currentWidget()
        self.current_tab_name = self.ui.tabWidget.tabText(
            self.ui.tabWidget.currentIndex())
        self.summary = False
        self.current_tab.axes.set_title(self.current_tab_name)

        # Data and plot info
        self.plot_ref_baseline = None
        self.plot_ref_hirise = None

        self.show()

    def make_summary_ui(self):
        self.peak_memory_stats = QLabel('0.00')
        self.bandwidth_stats = QLabel('0.00')
        self.energy_stats = QLabel('0.00')
        self.ui.formLayout.addRow(self.peak_memory_stats)
        self.ui.formLayout.addRow(self.bandwidth_stats)
        self.ui.formLayout.addRow(self.energy_stats)
        self.update_stats((0, 0, 0))

    def tab_changed(self):
        self.current_tab = self.ui.tabWidget.currentWidget()
        self.current_tab_name = self.ui.tabWidget.tabText(
            self.ui.tabWidget.currentIndex())
        if self.current_tab_name == 'Summary':
            self.summary = True
            self.update_stats(self.current_plot_data)
        else:
            self.summary = False
            self.current_tab.axes.clear()
            self.plot_ref_baseline = None
            self.plot_ref_hirise = None
            self.current_tab.axes.set_title(self.current_tab_name)
            self.update_plots(self.current_plot_data)

    def update_tab(self, data: tuple):
        if self.current_tab_name != 'Summary':
            self.update_plots(data)
        else:
            self.update_stats(data)

    def update_stats(self, stat_data: tuple = None):
        pm_now, pm_min, pm_max, pm_mean = [
            f'{np.random.random(): 0.3f}' for i in range(4)]
        band_now, band_min, band_max, band_mean = [
            f'{np.random.random(): 0.3f}' for i in range(4)]
        e_now, e_min, e_max, e_mean = [
            f'{np.random.random(): 0.3f}' for i in range(4)]
        self.peak_memory_stats.setText(
            'Peak Memory (Units):'
            + f'\n\t> Baseline:\n\t{pm_now} (now) {pm_min} (min) {pm_max} '
            + f'(max) {pm_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{pm_now} (now) {pm_min} (min) {pm_max} (max) '
            + f'{pm_mean} (mean)'
        )
        self.bandwidth_stats.setText(
            'Bandwidth (Units): '
            + f'\n\t> Baseline:\n\t{band_now} (now) {band_min} (min) '
            + f'{band_max} (max) {band_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{band_now} (now) {band_min} (min) '
            + f'{band_max} (max) {band_mean} (mean)'
        )
        self.energy_stats.setText(
            'Energy (Units): '
            + f'\n\t> Baseline:\n\t{e_now} (now) {e_min} (min) {e_max} (max) '
            + f'{e_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{e_now} (now) {e_min} (min) {e_max} (max) '
            + f'{e_mean} (mean)'
        )

    def update_plots(self, plot_data: tuple):
        self.current_plot_data = plot_data
        peak_memory, bandwidth, energy = plot_data
        # Temp data
        self.baseline_data = np.concatenate(
            (self.baseline_data[1:], np.random.randint(10, size=1)))
        self.hirise_data = np.concatenate(
            (self.hirise_data[1:], np.random.randint(10, size=1)))
        # Check if plot ref is None
        if self.plot_ref_baseline is None or self.plot_ref_hirise is None:
            plot_ref_baseline = self.current_tab.axes.plot(
                self.xdata, self.baseline_data, 'r'
            )
            plot_ref_hirise = self.current_tab.axes.plot(
                self.xdata, self.hirise_data, 'b'
            )
            self.plot_ref_baseline = plot_ref_baseline[0]
            self.plot_ref_hirise = plot_ref_hirise[0]
        else:
            self.plot_ref_baseline.set_ydata(self.baseline_data)
            self.plot_ref_hirise.set_ydata(self.hirise_data)
        self.current_tab.draw()
        # self.energyTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.bandwidthTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.peakMemoryTab.axes.plot([1,2,3], [1,2,3], 'r')
        # self.energyTab.draw()
        # self.bandwidthTab.draw()
        # self.peakMemoryTab.draw()

    def update_cameras(self, pixmaps: tuple):
        detect_pm, baseline_pm, hirise_pm = pixmaps
        self.pixmap = detect_pm
        disabledVideoSize = self.ui.disabledVideo.size()
        enabledVideoSize = self.ui.enabledVideo.size()
        detectVideoSize = self.ui.detectVideo.size()
        self.ui.detectVideo.setPixmap(detect_pm.scaled(
            detectVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.disabledVideo.setPixmap(baseline_pm.scaled(
            disabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.enabledVideo.setPixmap(hirise_pm.scaled(
            enabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
