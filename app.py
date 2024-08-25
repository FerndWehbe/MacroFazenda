import sys

import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow

from gui.ui_main import UIMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = UIMainWindow()
        self.ui.setup_ui(self)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    window = MainWindow()
    sys.exit(app.exec())
