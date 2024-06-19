"""_summary_
https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
"""

import time
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
        self.connect_signals()

        # Temp pixmap
        self.pixmap = QPixmap()

        # Temporary data
        self.current_plot_data = None
        self.xdata = np.arange(50)
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

        # Scale contents to GUI, set False to preserve images quality
        self.ui.detectVideo.setScaledContents(True)
        self.ui.disabledVideo.setScaledContents(True)
        self.ui.enabledVideo.setScaledContents(True)

        # Setup Tabs
        self.latencyTab: PlotCanvas = self.ui.latencyTab
        self.bandwidthTab: PlotCanvas = self.ui.bandwidthTab
        self.peakMemoryTab: PlotCanvas = self.ui.peakMemoryTab
        self.current_tab: PlotCanvas = self.ui.tabWidget.currentWidget()
        self.current_tab_name = self.ui.tabWidget.tabText(
            self.ui.tabWidget.currentIndex())
        self.tab_changed()

        # Data and plot info
        self.plot_ref_baseline = None
        self.plot_ref_baseline_c = None
        self.plot_ref_hirise = None

        # Set Camera tab
        self.ui.detectVideo.set_tab(self.current_tab_name)
        self.showFullScreen()

    def connect_signals(self):
        self.ui.detectVideo.update_frame.connect(self.update_cameras)
        self.ui.detectVideo.update_stats.connect(self.update_tab)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.ui.cameraResolutionSlider.valueChanged.connect(
            self.camera_resolution_changed
        )
        self.ui.detectionResolutionSlider.valueChanged.connect(
            self.detection_resolution_changed
        )
        self.ui.baselinePixelArraySlider.valueChanged.connect(
            self.baseline_pixel_array_changed
        )
        self.ui.hirisePixelArraySlider.valueChanged.connect(
            self.hirise_pixel_array_changed
        )
        self.ui.nextFace.clicked.connect(self.next_face)
        self.ui.previousFace.clicked.connect(self.previous_face)
        self.ui.resetFace.clicked.connect(self.reset_face)
        self.ui.detectVideo.hirise.update_num_heads.connect(
            self.update_num_heads_detected)

    def update_num_heads_detected(self, num_faces: int):
        self.ui.facesDetected.setText(f'Detected: {num_faces}')
        self.ui.currentIndex.setText(
            f'Current Index: {self.ui.detectVideo.hirise.focus_number}')

    def next_face(self):
        if self.ui.detectVideo.hirise.focus_number < self.ui.detectVideo.hirise.num_heads - 1:
            self.ui.detectVideo.hirise.focus_number += 1
            self.ui.currentIndex.setText(
                f'Current Index: {self.ui.detectVideo.hirise.focus_number}')

    def previous_face(self):
        if self.ui.detectVideo.hirise.focus_number > 0:
            self.ui.detectVideo.hirise.focus_number -= 1
            self.ui.currentIndex.setText(
                f'Current Index: {self.ui.detectVideo.hirise.focus_number}')

    def reset_face(self):
        self.ui.detectVideo.hirise.focus_number = 0
        self.ui.currentIndex.setText(
            f'Current Index: {self.ui.detectVideo.hirise.focus_number}')

    def camera_resolution_changed(self):
        camera_resolution_id = self.ui.cameraResolutionSlider.value()
        new_camera_resolution = \
            self.ui.detectVideo.hirise.change_camera_resolution(
                camera_resolution_id
            )
        self.ui.cameraResolutionValue.setText(
            f'Value: {new_camera_resolution}'
        )
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

    def detection_resolution_changed(self):
        detect_resolution_slider_id = self.ui.detectionResolutionSlider.value()
        new_detection_resolution = \
            self.ui.detectVideo.hirise.change_detection_resolution(
                detect_resolution_slider_id
            )
        self.ui.detectionResolutionValue.setText(
            f'Value: {new_detection_resolution}'
        )
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

    def baseline_pixel_array_changed(self):
        baseline_slider_id = self.ui.baselinePixelArraySlider.value()
        new_array_size = self.ui.detectVideo.hirise.change_baseline_array(
            baseline_slider_id
        )
        self.ui.baselinePixelArrayValue.setText(f'Value: {new_array_size}')
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

    def hirise_pixel_array_changed(self):
        hirise_slider_id = self.ui.hirisePixelArraySlider.value()
        new_array_size = self.ui.detectVideo.hirise.change_hirise_array(
            hirise_slider_id
        )
        self.ui.hirisePixelArrayValue.setText(f'Value: {new_array_size}')
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))

    def make_summary_ui(self):
        self.peak_memory_stats = QLabel('0.00')
        self.bandwidth_stats = QLabel('0.00')
        self.latency_stats = QLabel('0.00')
        self.ui.formLayout.addRow(self.peak_memory_stats)
        self.ui.formLayout.addRow(self.bandwidth_stats)
        self.ui.formLayout.addRow(self.latency_stats)

    def tab_changed(self):
        # Reset Data
        self.baseline_data = np.zeros((50,))
        self.baseline_data_c = np.zeros((50,))
        self.hirise_data = np.zeros((50,))
        # Change tab and call correct functions
        self.current_tab = self.ui.tabWidget.currentWidget()
        self.current_tab_name = self.ui.tabWidget.tabText(
            self.ui.tabWidget.currentIndex())
        self.ui.detectVideo.set_tab(self.current_tab_name)
        if self.current_tab_name == 'Settings':
            pass
        elif self.current_tab_name == 'Summary':
            self.update_stats(self.current_plot_data)
        else:
            self.current_tab.axes.clear()
            self.plot_ref_baseline = None
            self.plot_ref_baseline_c = None
            self.plot_ref_hirise = None
            self.current_tab.axes.set_title(self.current_tab_name)
            self.update_plots(self.current_plot_data)

    def update_tab(self, data: dict):
        if self.current_tab_name == 'Settings':
            pass
        elif self.current_tab_name == 'Summary':
            self.update_stats(data)
        else:
            # Set legends
            if self.current_tab_name != 'Latency':
                self.current_tab.axes.legend(
                    ['HiRISE', 'Baseline', 'Baseline Compressed'])
            else:
                self.current_tab.axes.legend(
                    ['TPU Inference Latency'])
            # Set Labels
            self.current_tab.axes.set_ylabel(
                data['hirise'][self.current_tab_name]['units'])
            self.current_tab.axes.set_xlabel(
                'Samples'
            )
            self.update_plots(data)

    def update_stats(self, stats: dict):
        if stats is None:
            return
        pm_now, pm_min, pm_max, pm_mean, pm_units = (
            stats['hirise']['Peak Memory']['now'],
            stats['hirise']['Peak Memory']['min'],
            stats['hirise']['Peak Memory']['max'],
            stats['hirise']['Peak Memory']['avg'],
            stats['hirise']['Peak Memory']['units']
        )
        band_now, band_min, band_max, band_mean, band_units = (
            stats['hirise']['Bandwidth']['now'],
            stats['hirise']['Bandwidth']['min'],
            stats['hirise']['Bandwidth']['max'],
            stats['hirise']['Bandwidth']['avg'],
            stats['hirise']['Bandwidth']['units']
        )
        l_now, l_min, l_max, l_mean, l_units = (
            stats['hirise']['Latency']['now'],
            stats['hirise']['Latency']['min'],
            stats['hirise']['Latency']['max'],
            stats['hirise']['Latency']['avg'],
            stats['hirise']['Latency']['units']
        )
        fps_now, fps_min, fps_max, fps_mean = (
            stats['hirise']['Latency']['fps_now'],
            stats['hirise']['Latency']['fps_min'],
            stats['hirise']['Latency']['fps_max'],
            stats['hirise']['Latency']['fps_avg'],
        )
        b_pm_now, b_pm_min, b_pm_max, b_pm_mean = (
            stats['baseline']['Peak Memory']['now'],
            stats['baseline']['Peak Memory']['min'],
            stats['baseline']['Peak Memory']['max'],
            stats['baseline']['Peak Memory']['avg'],
        )
        bc_band_now, bc_band_min, bc_band_max, bc_band_mean = (
            stats['baseline']['Bandwidth']['c_now'],
            stats['baseline']['Bandwidth']['c_min'],
            stats['baseline']['Bandwidth']['c_max'],
            stats['baseline']['Bandwidth']['c_avg'],
        )
        b_band_now, b_band_min, b_band_max, b_band_mean = (
            stats['baseline']['Bandwidth']['now'],
            stats['baseline']['Bandwidth']['min'],
            stats['baseline']['Bandwidth']['max'],
            stats['baseline']['Bandwidth']['avg'],
        )
        self.peak_memory_stats.setText(
            f'Peak Memory ({pm_units}):'
            + f'\n\t> Baseline:\n\t{b_pm_now} (now) {b_pm_min} (min) {b_pm_max}'
            + f' (max) {b_pm_mean:.3f} (mean)\n'
            + f'\t> HiRISE:\n\t{pm_now} (now) {pm_min} (min) {pm_max} (max) '
            + f'{pm_mean:.3f} (mean)\n'
        )
        self.bandwidth_stats.setText(
            f'Bandwidth ({band_units}): '
            + f'\n\t> Baseline Original:\n\t{b_band_now} (now) '
            + f'{b_band_min} (min) {b_band_max} (max) {b_band_mean} (mean)\n'
            + f'\t> Baseline Compressed:\n\t{bc_band_now} (now) '
            + f'{bc_band_min} (min) {bc_band_max} (max) '
            + f'{bc_band_mean:.3f} (mean)\n'
            + f'\t> HiRISE:\n\t{band_now} (now) {band_min} (min) '
            + f'{band_max} (max) {band_mean:.3f} (mean)\n'
        )
        self.latency_stats.setText(
            f'Latency ({l_units}): '
            + f'\n\t{l_now:.3f} (now) {l_min:.3f} (min) {l_max:.3f} (max) '
            + f'{l_mean:.3f} (mean)'
            f'\n\nLatency (FPS): '
            + f'\n\t{fps_now:.1f} (now) {fps_min:.1f} (min) {fps_max:.1f} (max) '
            + f'{fps_mean:.1f} (mean)'
        )

    def update_plots(self, plot_data: dict):
        if plot_data is None:
            return
        # Extract data, pop oldest point, and push newest data point into array
        if self.current_tab_name != 'Latency':
            self.baseline_data_c = np.concatenate((
                self.baseline_data_c[1:],
                np.array([plot_data['baseline'][self.current_tab_name]['c_now']])
            ))
            self.baseline_data = np.concatenate((
                self.baseline_data[1:],
                np.array([plot_data['baseline'][self.current_tab_name]['now']])
            ))
        self.hirise_data = np.concatenate((
            self.hirise_data[1:],
            np.array([plot_data['hirise'][self.current_tab_name]['now']])
        ))
        # Check if plot ref is None
        if (
            self.plot_ref_baseline is None and
            self.plot_ref_baseline_c is None and
            self.plot_ref_hirise is None
        ):
            # Plot hirise line
            plot_ref_hirise = self.current_tab.axes.plot(
                self.xdata, self.hirise_data, 'g'
            )
            self.plot_ref_hirise = plot_ref_hirise[0]
            # Plot the baseline lines
            if self.current_tab_name != 'Latency':
                plot_ref_baseline = self.current_tab.axes.plot(
                    self.xdata, self.baseline_data, 'r'
                )
                plot_ref_baseline_c = self.current_tab.axes.plot(
                    self.xdata, self.baseline_data_c, 'b'
                )
                self.plot_ref_baseline_c = plot_ref_baseline_c[0]
                self.plot_ref_baseline = plot_ref_baseline[0]
        else:
            if self.current_tab_name != 'Latency':
                self.plot_ref_baseline_c.set_ydata(self.baseline_data_c)
                self.plot_ref_baseline.set_ydata(self.baseline_data)
            self.plot_ref_hirise.set_ydata(self.hirise_data)
        # Rescale the y-axis according to data
        self.current_tab.axes.relim()
        self.current_tab.axes.autoscale_view()
        # Redraw
        self.current_tab.draw()

    def update_cameras(self, pixmaps: tuple):
        # print(f'Received Frame: {time.time()}')
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
        # print(f'Done Time: {time.time()}')
