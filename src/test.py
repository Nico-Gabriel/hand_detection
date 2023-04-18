import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu


def new_file():
    print("New...")


def open_file():
    print("Open...")


def save_file():
    print("Save...")


def export_file_as_image():
    print("Export as image...")


def export_file_as_whiteboard():
    print("Export as whiteboard...")


class TestWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.create_menu_bar()

    def create_menu_bar(self):
        new_file_action = QAction("New...", self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.triggered.connect(new_file)

        open_file_action = QAction("Open...", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(open_file)

        save_file_action = QAction("Save...", self)
        save_file_action.setShortcut("Ctrl+S")
        save_file_action.triggered.connect(save_file)

        export_file_as_image_action = QAction("Export as image...", self)
        export_file_as_image_action.setShortcut("Ctrl+E")
        export_file_as_image_action.triggered.connect(export_file_as_image)

        export_file_as_whiteboard_action = QAction("Export as whiteboard...", self)
        export_file_as_whiteboard_action.setShortcut("Ctrl+Shift+E")
        export_file_as_whiteboard_action.triggered.connect(export_file_as_whiteboard)

        export_file_menu = QMenu("Export", self)
        export_file_menu.addAction(export_file_as_image_action)
        export_file_menu.addAction(export_file_as_whiteboard_action)

        file_menu = QMenu("File", self)
        file_menu.addAction(new_file_action)
        file_menu.addSeparator()
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addSeparator()
        file_menu.addMenu(export_file_menu)

        self.menuBar().addMenu(file_menu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
