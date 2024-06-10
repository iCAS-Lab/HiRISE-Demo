import sys

from PySide6.QtWidgets import QApplication
import PySide6.QtGui
from gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(app.primaryScreen().size().toTuple())
    main_window = MainWindow()
    main_window.resize(1920,1080)
    sys.exit(app.exec())
