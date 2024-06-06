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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

from camera import Camera
from plot import PlotCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1129, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"")
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
        self.peakMemoryTab = QWidget()
        self.peakMemoryTab.setObjectName(u"peakMemoryTab")
        self.gridLayout_4 = QGridLayout(self.peakMemoryTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.peakMemoryWidget = PlotCanvas(self.peakMemoryTab)
        self.peakMemoryWidget.setObjectName(u"peakMemoryWidget")

        self.gridLayout_4.addWidget(self.peakMemoryWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.peakMemoryTab, "")
        self.bandwidthTab = QWidget()
        self.bandwidthTab.setObjectName(u"bandwidthTab")
        self.gridLayout_2 = QGridLayout(self.bandwidthTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bandwidthWidget = PlotCanvas(self.bandwidthTab)
        self.bandwidthWidget.setObjectName(u"bandwidthWidget")

        self.gridLayout_2.addWidget(self.bandwidthWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.bandwidthTab, "")
        self.energyTab = QWidget()
        self.energyTab.setObjectName(u"energyTab")
        self.gridLayout_3 = QGridLayout(self.energyTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.energyWidget = PlotCanvas(self.energyTab)
        self.energyWidget.setObjectName(u"energyWidget")

        self.gridLayout_3.addWidget(self.energyWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.energyTab, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HiRISE Demo", None))
        self.detectLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700;\">Face Detection</span></p></body></html>", None))
        self.detectVideo.setText("")
        self.disabledLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700;\">HiRISE Disabled</span></p></body></html>", None))
        self.disabledVideo.setText("")
        self.enabledLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700;\">HiRISE Enabled</span></p></body></html>", None))
        self.enabledVideo.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700;\">Realtime Statistics</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.peakMemoryTab), QCoreApplication.translate("MainWindow", u"Peak Memory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bandwidthTab), QCoreApplication.translate("MainWindow", u"Bandwidth", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.energyTab), QCoreApplication.translate("MainWindow", u"Energy", None))
    # retranslateUi

