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
        self.current_plot_data = None
        self.xdata = np.arange(50)
        self.baseline_data = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

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

        # Set Camera tab
        self.ui.detectVideo.set_tab(self.current_tab_name)

        self.show()

    def make_summary_ui(self):
        self.peak_memory_stats = QLabel('0.00')
        self.bandwidth_stats = QLabel('0.00')
        self.energy_stats = QLabel('0.00')
        self.ui.formLayout.addRow(self.peak_memory_stats)
        self.ui.formLayout.addRow(self.bandwidth_stats)
        self.ui.formLayout.addRow(self.energy_stats)

    def tab_changed(self):
        # Reset Data
        self.baseline_data = np.zeros((50,))
        self.hirise_data = np.zeros((50,))
        # Change tab and call correct functions
        self.current_tab = self.ui.tabWidget.currentWidget()
        self.current_tab_name = self.ui.tabWidget.tabText(
            self.ui.tabWidget.currentIndex())
        self.ui.detectVideo.set_tab(self.current_tab_name)
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

    def update_tab(self, data: dict):
        if self.current_tab_name != 'Summary':
            self.update_plots(data)
        else:
            self.update_stats(data)

    def update_stats(self, stats: dict):
        if stats is None:
            return
        pm_now, pm_min, pm_max, pm_mean = (
            stats['hirise']['Peak Memory']['now'],
            stats['hirise']['Peak Memory']['min'],
            stats['hirise']['Peak Memory']['max'],
            stats['hirise']['Peak Memory']['avg']
        )
        band_now, band_min, band_max, band_mean = (
            stats['hirise']['Bandwidth']['now'],
            stats['hirise']['Bandwidth']['min'],
            stats['hirise']['Bandwidth']['max'],
            stats['hirise']['Bandwidth']['avg'],
        )
        e_now, e_min, e_max, e_mean = (
            stats['hirise']['Energy']['now'],
            stats['hirise']['Energy']['min'],
            stats['hirise']['Energy']['max'],
            stats['hirise']['Energy']['avg'],
        )
        b_pm_now, b_pm_min, b_pm_max, b_pm_mean = (
            stats['baseline']['Peak Memory']['now'],
            stats['baseline']['Peak Memory']['min'],
            stats['baseline']['Peak Memory']['max'],
            stats['baseline']['Peak Memory']['avg'],
        )
        b_band_now, b_band_min, b_band_max, b_band_mean = (
            stats['baseline']['Bandwidth']['now'],
            stats['baseline']['Bandwidth']['min'],
            stats['baseline']['Bandwidth']['max'],
            stats['baseline']['Bandwidth']['avg'],
        )
        b_e_now, b_e_min, b_e_max, b_e_mean = (
            stats['baseline']['Energy']['now'],
            stats['baseline']['Energy']['min'],
            stats['baseline']['Energy']['max'],
            stats['baseline']['Energy']['avg'],
        )
        self.peak_memory_stats.setText(
            'Peak Memory (Units):'
            + f'\n\t> Baseline:\n\t{b_pm_now} (now) {b_pm_min} (min) {b_pm_max}'
            + f' (max) {b_pm_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{pm_now} (now) {pm_min} (min) {pm_max} (max) '
            + f'{pm_mean} (mean)'
        )
        self.bandwidth_stats.setText(
            'Bandwidth (Units): '
            + f'\n\t> Baseline:\n\t{b_band_now} (now) {b_band_min} (min) '
            + f'{b_band_max} (max) {b_band_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{band_now} (now) {band_min} (min) '
            + f'{band_max} (max) {band_mean} (mean)'
        )
        self.energy_stats.setText(
            'Energy (Units): '
            + f'\n\t> Baseline:\n\t{b_e_now} (now) {b_e_min} (min) '
            + f'{b_e_max} (max) {b_e_mean} (mean)\n'
            + f'\t> HiRISE:\n\t{e_now} (now) {e_min} (min) {e_max} (max) '
            + f'{e_mean} (mean)'
        )

    def update_plots(self, plot_data: dict):
        if plot_data is None:
            return
        # Extract Data
        self.baseline_data = np.concatenate((
            self.baseline_data[1:],
            np.array([plot_data['baseline'][self.current_tab_name]['now']])
        ))
        self.hirise_data = np.concatenate((
            self.hirise_data[1:],
            np.array([plot_data['hirise'][self.current_tab_name]['now']])
        ))
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
        self.current_tab.axes.legend(['Baseline', 'HiRISE'])
        self.current_tab.draw()

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
