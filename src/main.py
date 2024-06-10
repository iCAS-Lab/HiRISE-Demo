import sys

from PySide6.QtWidgets import QApplication
from gui import MainWindow

if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    sys.exit(app.exec())