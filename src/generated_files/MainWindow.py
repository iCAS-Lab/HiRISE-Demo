# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QTabWidget, QVBoxLayout, QWidget)

from camera import Camera
from plot import PlotCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 887)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"background-color: rgb(92, 92, 92);")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.detect = QFrame(self.centralwidget)
        self.detect.setObjectName(u"detect")
        sizePolicy.setHeightForWidth(self.detect.sizePolicy().hasHeightForWidth())
        self.detect.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.detect)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.detectLabel = QLabel(self.detect)
        self.detectLabel.setObjectName(u"detectLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.detectLabel.sizePolicy().hasHeightForWidth())
        self.detectLabel.setSizePolicy(sizePolicy1)
        self.detectLabel.setMaximumSize(QSize(16777215, 64))
        self.detectLabel.setStyleSheet(u"background-color: rgb(115, 0, 10);")
        self.detectLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.detectLabel)

        self.detectVideo = Camera(self.detect)
        self.detectVideo.setObjectName(u"detectVideo")
        sizePolicy.setHeightForWidth(self.detectVideo.sizePolicy().hasHeightForWidth())
        self.detectVideo.setSizePolicy(sizePolicy)
        self.detectVideo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.detectVideo)


        self.gridLayout.addWidget(self.detect, 0, 0, 1, 1)

        self.disabledFrame = QFrame(self.centralwidget)
        self.disabledFrame.setObjectName(u"disabledFrame")
        sizePolicy.setHeightForWidth(self.disabledFrame.sizePolicy().hasHeightForWidth())
        self.disabledFrame.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.disabledFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.disabledLabel = QLabel(self.disabledFrame)
        self.disabledLabel.setObjectName(u"disabledLabel")
        sizePolicy1.setHeightForWidth(self.disabledLabel.sizePolicy().hasHeightForWidth())
        self.disabledLabel.setSizePolicy(sizePolicy1)
        self.disabledLabel.setMaximumSize(QSize(16777215, 64))
        self.disabledLabel.setStyleSheet(u"background-color: rgb(115, 0, 10);")
        self.disabledLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.disabledLabel)

        self.disabledVideo = QLabel(self.disabledFrame)
        self.disabledVideo.setObjectName(u"disabledVideo")
        sizePolicy.setHeightForWidth(self.disabledVideo.sizePolicy().hasHeightForWidth())
        self.disabledVideo.setSizePolicy(sizePolicy)
        self.disabledVideo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.disabledVideo)


        self.gridLayout.addWidget(self.disabledFrame, 0, 1, 1, 1)

        self.enabledFrame = QFrame(self.centralwidget)
        self.enabledFrame.setObjectName(u"enabledFrame")
        sizePolicy.setHeightForWidth(self.enabledFrame.sizePolicy().hasHeightForWidth())
        self.enabledFrame.setSizePolicy(sizePolicy)
        self.verticalLayout_7 = QVBoxLayout(self.enabledFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.enabledLabel = QLabel(self.enabledFrame)
        self.enabledLabel.setObjectName(u"enabledLabel")
        sizePolicy1.setHeightForWidth(self.enabledLabel.sizePolicy().hasHeightForWidth())
        self.enabledLabel.setSizePolicy(sizePolicy1)
        self.enabledLabel.setMaximumSize(QSize(16777215, 64))
        self.enabledLabel.setStyleSheet(u"background-color: rgb(115, 0, 10);")
        self.enabledLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.enabledLabel)

        self.enabledVideo = QLabel(self.enabledFrame)
        self.enabledVideo.setObjectName(u"enabledVideo")
        sizePolicy.setHeightForWidth(self.enabledVideo.sizePolicy().hasHeightForWidth())
        self.enabledVideo.setSizePolicy(sizePolicy)
        self.enabledVideo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.enabledVideo)


        self.gridLayout.addWidget(self.enabledFrame, 1, 1, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgb(115, 0, 10);")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-weight: bold;\n"
"font-size: 16px;")
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(False)
        self.peakMemoryTab = PlotCanvas()
        self.peakMemoryTab.setObjectName(u"peakMemoryTab")
        self.gridLayout_4 = QGridLayout(self.peakMemoryTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget.addTab(self.peakMemoryTab, "")
        self.bandwidthTab = PlotCanvas()
        self.bandwidthTab.setObjectName(u"bandwidthTab")
        self.gridLayout_2 = QGridLayout(self.bandwidthTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget.addTab(self.bandwidthTab, "")
        self.latencyTab = PlotCanvas()
        self.latencyTab.setObjectName(u"latencyTab")
        self.gridLayout_3 = QGridLayout(self.latencyTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget.addTab(self.latencyTab, "")
        self.summaryTab = QWidget()
        self.summaryTab.setObjectName(u"summaryTab")
        self.gridLayout_5 = QGridLayout(self.summaryTab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.gridLayout_5.addLayout(self.formLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.summaryTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.formLayout_3 = QFormLayout(self.settingsTab)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.resolutionSlider = QSlider(self.settingsTab)
        self.resolutionSlider.setObjectName(u"resolutionSlider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.resolutionSlider.sizePolicy().hasHeightForWidth())
        self.resolutionSlider.setSizePolicy(sizePolicy2)
        self.resolutionSlider.setMinimum(0)
        self.resolutionSlider.setMaximum(10)
        self.resolutionSlider.setSingleStep(1)
        self.resolutionSlider.setPageStep(1)
        self.resolutionSlider.setValue(1)
        self.resolutionSlider.setSliderPosition(1)
        self.resolutionSlider.setOrientation(Qt.Horizontal)
        self.resolutionSlider.setTickPosition(QSlider.TicksBelow)
        self.resolutionSlider.setTickInterval(1)

        self.gridLayout_6.addWidget(self.resolutionSlider, 2, 1, 1, 1)

        self.poolingSlider = QSlider(self.settingsTab)
        self.poolingSlider.setObjectName(u"poolingSlider")
        sizePolicy2.setHeightForWidth(self.poolingSlider.sizePolicy().hasHeightForWidth())
        self.poolingSlider.setSizePolicy(sizePolicy2)
        self.poolingSlider.setMinimum(0)
        self.poolingSlider.setMaximum(4)
        self.poolingSlider.setSingleStep(1)
        self.poolingSlider.setPageStep(1)
        self.poolingSlider.setValue(2)
        self.poolingSlider.setOrientation(Qt.Horizontal)
        self.poolingSlider.setTickPosition(QSlider.TicksBelow)
        self.poolingSlider.setTickInterval(1)

        self.gridLayout_6.addWidget(self.poolingSlider, 0, 1, 1, 1)

        self.poolingSizeLabel = QLabel(self.settingsTab)
        self.poolingSizeLabel.setObjectName(u"poolingSizeLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.poolingSizeLabel.sizePolicy().hasHeightForWidth())
        self.poolingSizeLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.poolingSizeLabel, 0, 0, 1, 1)

        self.boundingBoxIndexLabel = QLabel(self.settingsTab)
        self.boundingBoxIndexLabel.setObjectName(u"boundingBoxIndexLabel")
        sizePolicy3.setHeightForWidth(self.boundingBoxIndexLabel.sizePolicy().hasHeightForWidth())
        self.boundingBoxIndexLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.boundingBoxIndexLabel, 3, 0, 1, 1)

        self.resolutionLabel = QLabel(self.settingsTab)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.resolutionLabel.sizePolicy().hasHeightForWidth())
        self.resolutionLabel.setSizePolicy(sizePolicy4)

        self.gridLayout_6.addWidget(self.resolutionLabel, 2, 0, 1, 1)

        self.resolutionValue = QLabel(self.settingsTab)
        self.resolutionValue.setObjectName(u"resolutionValue")

        self.gridLayout_6.addWidget(self.resolutionValue, 2, 2, 1, 1)

        self.poolValue = QLabel(self.settingsTab)
        self.poolValue.setObjectName(u"poolValue")

        self.gridLayout_6.addWidget(self.poolValue, 0, 2, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.nextFace = QPushButton(self.settingsTab)
        self.nextFace.setObjectName(u"nextFace")

        self.gridLayout_7.addWidget(self.nextFace, 0, 1, 1, 1)

        self.previousFace = QPushButton(self.settingsTab)
        self.previousFace.setObjectName(u"previousFace")

        self.gridLayout_7.addWidget(self.previousFace, 0, 0, 1, 1)

        self.resetFace = QPushButton(self.settingsTab)
        self.resetFace.setObjectName(u"resetFace")

        self.gridLayout_7.addWidget(self.resetFace, 1, 0, 1, 2)


        self.gridLayout_6.addLayout(self.gridLayout_7, 3, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.facesDetected = QLabel(self.settingsTab)
        self.facesDetected.setObjectName(u"facesDetected")

        self.verticalLayout_2.addWidget(self.facesDetected)

        self.currentIndex = QLabel(self.settingsTab)
        self.currentIndex.setObjectName(u"currentIndex")

        self.verticalLayout_2.addWidget(self.currentIndex)


        self.gridLayout_6.addLayout(self.verticalLayout_2, 3, 2, 1, 1)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.gridLayout_6)

        self.tabWidget.addTab(self.settingsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HiRISE Demo", None))
        self.detectLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700; color:#ffffff;\">Face Detection</span></p></body></html>", None))
        self.detectVideo.setText("")
        self.disabledLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700; color:#ffffff;\">HiRISE Disabled (Baseline)</span></p></body></html>", None))
        self.disabledVideo.setText("")
        self.enabledLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700; color:#ffffff;\">HiRISE Enabled</span></p></body></html>", None))
        self.enabledVideo.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700; color:#ffffff;\">Realtime Statistics</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.peakMemoryTab), QCoreApplication.translate("MainWindow", u"Peak Memory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bandwidthTab), QCoreApplication.translate("MainWindow", u"Bandwidth", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.latencyTab), QCoreApplication.translate("MainWindow", u"Latency", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.summaryTab), QCoreApplication.translate("MainWindow", u"Summary", None))
        self.poolingSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Pooling Size", None))
        self.boundingBoxIndexLabel.setText(QCoreApplication.translate("MainWindow", u"Person Index", None))
        self.resolutionLabel.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.resolutionValue.setText(QCoreApplication.translate("MainWindow", u"Value: (640, 480)", None))
        self.poolValue.setText(QCoreApplication.translate("MainWindow", u"Value: 96", None))
        self.nextFace.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.previousFace.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.resetFace.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.facesDetected.setText(QCoreApplication.translate("MainWindow", u"Detected:", None))
        self.currentIndex.setText(QCoreApplication.translate("MainWindow", u"Current Index: 0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

