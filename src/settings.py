"""
Settings

This script is needed for the settings in the drawing board application.

After importing this script as a module, the settings can be accessed by
initializing an instance of the SettingsWindow class.

It is required that 'PyQt6' is installed.

Author: Nico-Gabriel Ruckendorfer
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QColorDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton


class SettingsWindow(QDialog):
    """
    Settings Window

    This class is used to create a settings window, which allows the user to
    change the line thickness and color of the lines drawn on the virtual
    drawing board application.

    The visibility of the settings window can be toggled by calling the show()
    or close() method of the instance.

    Methods
    -------
    init()
        Initializes the settings window.
    create_layout()
        Creates the layout of the settings window.
    create_line_thickness_layout()
        Creates the layout for the line thickness settings.
    create_line_color_layout()
        Creates the layout for the line color settings.
    change_line_thickness(label, value)
        Changes the line thickness of the lines drawn on the virtual drawing
        board.
    change_line_color()
        Changes the line color of the lines drawn on the virtual drawing board.
    """

    def __init__(self):
        """
        Initializes the settings window.
        """

        super().__init__()
        self.setWindowTitle("Settings")
        self.move(self.geometry().topLeft())
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.line_thickness = 10
        self.line_color = (255, 0, 0)
        self.create_layout()

    def create_layout(self):
        """
        Creates the layout of the settings window.

        The layout consists of two layouts, one for the line thickness settings
        and one for the line color settings.
        """

        layout = QVBoxLayout()
        layout.addLayout(self.create_line_thickness_layout())
        layout.addLayout(self.create_line_color_layout())
        self.setLayout(layout)

    def create_line_thickness_layout(self) -> QVBoxLayout:
        """
        Creates the layout for the line thickness settings.

        :return: The layout for the line thickness settings.
        """

        lt_header = QLabel("Line thickness")
        lt_header.setFont(QFont("Courier New", 18))

        lt_label = QLabel(f"{self.line_thickness}")
        lt_label.setFont(QFont("Courier New", 18))
        lt_label.setFixedWidth(32)

        lt_slider = QSlider(Qt.Orientation.Horizontal)
        lt_slider.setMinimum(2)
        lt_slider.setMaximum(100)
        lt_slider.setTickInterval(1)
        lt_slider.setValue(self.line_thickness)
        lt_slider.valueChanged.connect(lambda: self.change_line_thickness(lt_label, lt_slider.value()))

        lt_property_layout = QHBoxLayout()
        lt_property_layout.addWidget(lt_slider)
        lt_property_layout.addWidget(lt_label)

        lt_layout = QVBoxLayout()
        lt_layout.addWidget(lt_header)
        lt_layout.addLayout(lt_property_layout)

        return lt_layout

    def create_line_color_layout(self) -> QVBoxLayout:
        """
        Creates the layout for the line color settings.

        :return: The layout for the line color settings.
        """

        lc_header = QLabel("Line color")
        lc_header.setFont(QFont("Courier New", 18))

        lc_label = QLabel("●")
        lc_label.setStyleSheet(f"color: rgb{self.line_color}; font-size: 24px")
        lc_label.setFixedWidth(32)

        lc_button = QPushButton("change color")
        lc_button.clicked.connect(lambda: self.change_line_color(lc_label))

        lc_property_layout = QHBoxLayout()
        lc_property_layout.addWidget(lc_button)
        lc_property_layout.addWidget(lc_label)

        lc_layout = QVBoxLayout()
        lc_layout.addWidget(lc_header)
        lc_layout.addLayout(lc_property_layout)

        return lc_layout

    def change_line_thickness(self, label: QLabel, value: int):
        """
        Changes the line thickness of the lines drawn on the virtual drawing board.

        :param label: The label that displays the line thickness.
        :param value: The new line thickness.
        """

        self.line_thickness = value
        label.setText(f"{self.line_thickness}")

    def change_line_color(self, label: QLabel):
        """
        Changes the line color of the lines drawn on the virtual drawing board.

        The value of the new line color is chosen using a color picker.

        :param label: The label that displays the line color.
        """

        color = QColorDialog().getColor()
        if color.isValid():
            self.line_color = (color.red(), color.green(), color.blue())
            label.setStyleSheet(f"color: rgb{self.line_color}; font-size: 24px")


# Only executed when this script is called directly from this file,
# not when it is imported as a module:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
