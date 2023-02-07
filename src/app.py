"""
Virtual Drawing Board

This program allows the user to draw on the virtual drawing board by painting
in the air with his index finger.

The MediaPipe Hands module is used to detect the position of the index
fingertip from the webcam input.

The OpenCV library is used to edit the webcam snapshot and draw the lines on
the virtual drawing board based on the previously detected indexfinger tip
positions.

It is required that 'opencv-python', 'mediapipe' and 'PyQt6' are installed.

Author: Nico-Gabriel Ruckendorfer
"""

from pathlib import Path

import cv2
import mediapipe as mp
from PyQt6 import QtGui
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QFileDialog

from settings import *


class VideoThread(QThread):
    """
    Video Thread

    This class is used to create a thread, which is used to detect the index
    fingertip position from the webcam input and draw the lines on the virtual
    drawing board.

    There is as well a circle around the active index fingertip, which is used
    to indicate the position of the index fingertip, with wich the user can
    draw.

    Also, the thread contains the logic methods for the different options
    (listed in the description of the MainWindow class), and emits a signal
    with the edited webcam snapshot, which is used to update the virtual
    drawing board in the main window class.

    Attributes
    ----------
    signal : pyqtSignal
        Signal, which is emitted when the thread is running and the webcam
        snapshot is edited.

    Methods
    -------
    init()
        Initializes the video thread.
    run()
        Runs as long as the thread is running. In this method, the logic for
        detecting the index fingertip position, editing the webcam snapshot,
        and emitting the signal is implemented.
    check_if_index_finger_is_up(landmarks) -> bool
        Checks if the index finger is up.
    get_coordinates(landmarks, image_width, image_height) -> tuple
        Returns the coordinates of the index fingertip.
    add_line(x, y)
        Adds a new line to the list of lines.
    draw_lines(image)
        Draws the lines stored in the list of lines on the webcam snapshot.
    draw_circle(image, x, y)
        Draws a circle around the active index fingertip.
    emit_signal(image)
        Emits the signal with the edited webcam snapshot.
    toggle_draw()
        Toggle whether the lines should be drawn on the webcam snapshot or not.
    undo()
        Removes the last line from the list of lines.
    clear()
        Removes all lines from the list of lines.
    check_for_new_line()
        Checks if a new line should be added to the list of lines.
    save()
        Save the current snapshot of the virtual drawing board as an image
        (*.png, *.jpg, *.jpeg) to the chosen path.
    stop()
        Stops the video thread.
    """

    signal = pyqtSignal(list)

    def __init__(self):
        """
        Initializes the video thread.
        """

        super().__init__()
        self.run_video_thread = True
        self.video = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.index_finger_tip = self.mp_hands.HandLandmark.INDEX_FINGER_TIP
        self.lines = [[]]
        self.draw = True
        self.board = None

    def run(self):
        """
        Runs as long as the thread is running. In this method, the logic for
        detecting the index fingertip position, editing the webcam snapshot,
        and emitting the signal is implemented.
        """

        with self.mp_hands.Hands(max_num_hands=1) as hands:
            while self.run_video_thread:
                success, image = self.video.read()
                image_height, image_width, _ = image.shape
                result = hands.process(image).multi_hand_landmarks
                if result:
                    landmarks = result[0].landmark
                    is_index_finger_up = self.check_if_index_finger_is_up(landmarks)
                    if is_index_finger_up:
                        x, y = self.get_coordinates(landmarks, image_width, image_height)
                        if self.draw:
                            self.add_line(x, y)
                else:
                    self.check_for_new_line()
                self.draw_lines(image)
                self.board = cv2.flip(image, 1)
                if result and is_index_finger_up:
                    self.draw_circle(image, x, y)
                if success:
                    self.emit_signal(image, image_height, image_width)
        self.video.release()

    def check_if_index_finger_is_up(self, landmarks) -> bool:
        """
        Checks if the index finger is up.

        :param landmarks: List of landmarks of the index finger.
        :return: True if the index finger is up, False otherwise.
        """

        for landmark in landmarks:
            if landmark.y >= landmarks[self.index_finger_tip].y:
                continue
            self.check_for_new_line()
            return False
        return True

    def get_coordinates(self, landmarks, image_width, image_height) -> tuple[int, int]:
        """
        Returns the coordinates of the index fingertip.

        :param landmarks: List of landmarks of the index finger.
        :param image_width: Width of the webcam snapshot.
        :param image_height: Height of the webcam snapshot.
        :return: Tuple of the x and y coordinates of the index fingertip.
        """

        x = int(landmarks[self.index_finger_tip].x * image_width)
        y = int(landmarks[self.index_finger_tip].y * image_height)
        return x, y

    def add_line(self, x, y):
        """
        Adds a new line to the list of lines.

        :param x: X coordinate of the index fingertip.
        :param y: Y coordinate of the index fingertip.
        """

        self.lines[len(self.lines) - 1].append([(x, y), settings.line_thickness, settings.line_color])

    def draw_lines(self, image):
        """
        Draws the lines stored in the list of lines on the webcam snapshot.

        :param image: Current webcam snapshot.
        """

        for line in self.lines:
            for i in range(len(line)):
                if i == 0:
                    continue
                cv2.line(image, line[i - 1][0], line[i][0], tuple(reversed(line[i - 1][2])), line[i - 1][1])

    @staticmethod
    def draw_circle(image, x, y):
        """
        Draws a circle around the active index fingertip.

        :param image: Current webcam snapshot.
        :param x: X coordinate of the index fingertip.
        :param y: Y coordinate of the index fingertip.
        """

        cv2.circle(image, (x, y), 50, tuple(reversed(settings.line_color)), 10)

    def emit_signal(self, image, image_height, image_width):
        """
        Emits the signal with the edited webcam snapshot.

        :param image: Current webcam snapshot.
        :param image_height: Height of the webcam snapshot.
        :param image_width: Width of the webcam snapshot.
        """

        self.signal.emit([cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB), image_height, image_width])

    def toggle_draw(self, label: QLabel, button: QPushButton):
        """
        Toggle whether the lines should be drawn on the webcam snapshot or not.

        :param label: Label that displays the current state of the drawing.
        :param button: Button that toggles the drawing mode.
        """

        self.draw = not self.draw
        self.check_for_new_line()
        label.setText(f"Drawing: {'ON' if self.draw else 'OFF'}")
        button.setText("Disable" if self.draw else "Enable")

    def undo(self):
        """
        Removes the last line from the list of lines.
        """

        delete_number = 1 if self.lines[len(self.lines) - 1] else 2
        self.lines = self.lines[:-delete_number]
        self.check_for_new_line() if self.lines else self.clear()

    def clear(self):
        """
        Removes all lines from the list of lines.
        """

        self.lines = [[]]

    def check_for_new_line(self):
        """
        Checks if a new line should be added to the list of lines.
        """

        if self.lines[len(self.lines) - 1]:
            self.lines.append([])

    def save(self):
        """
        Save the current snapshot of the virtual drawing board as an image
        (*.png, *.jpg, *.jpeg) to the chosen path.
        """

        image = self.board
        path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Image",
            f"{str(Path.home())}/Documents/Drawing.png",
            "Image (*.png *.jpg *.jpeg)"
        )
        if path:
            cv2.imwrite(path, image)

    def stop(self):
        """
        Stops the video thread.
        """

        self.run_video_thread = False
        self.wait()


class MainWindow(QWidget):
    """
    Main Window

    This is the main window of the virtual drawing board application, with the
    webcam video and the following options:
    - Drawing: ON/OFF
    - Undo
    - Clear
    - Settings
    - Save

    Methods
    -------
    init()
        Initializes the main window.
    create_layout()
        Creates the layout of the main window.
    create_options_layout()
        Creates the layout for the options.
    update_image(image, image_height, image_width)
        Updates the image of the webcam video.
    closeEvent(event)
        Closes the application.
    """

    def __init__(self):
        """
        Initializes the main window.
        """

        super().__init__()
        self.setWindowTitle("Virtual Drawing Board")
        self.move(self.geometry().topLeft())
        self.display_width = 1280
        self.display_height = 960
        self.video = QLabel()
        self.video.resize(self.display_width, self.display_height)
        self.create_layout()
        self.thread = VideoThread()
        self.thread.signal.connect(self.update_image)
        self.thread.start()

    def create_layout(self):
        """
        Creates the layout of the main window.

        The layout consists of the webcam video and the options.
        """

        layout = QVBoxLayout()
        layout.addWidget(self.video)
        layout.addLayout(self.create_options_layout())

        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedWidth(self.display_width)

        view = QVBoxLayout()
        view.addWidget(widget)
        view.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(view)

    def create_options_layout(self) -> QHBoxLayout:
        """
        Creates the layout for the options.

        :return: The layout for the options.
        """

        drawing_label = QLabel("Drawing: ON")
        drawing_label.setFont(QFont("Courier New", 18))
        drawing_label.setFixedWidth(134)

        drawing_button = QPushButton("Disable")
        drawing_button.clicked.connect(lambda: self.thread.toggle_draw(drawing_label, drawing_button))

        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(lambda: self.thread.undo())

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.thread.clear())

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(lambda: settings.show())

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.thread.save())

        buttons = [drawing_button, undo_button, clear_button, settings_button, save_button]

        options_layout = QHBoxLayout()
        options_layout.addWidget(drawing_label)

        # Shorter way to add the buttons to the layout with the set properties
        # and a stretch inbetween.
        for i in range(len(buttons)):
            buttons[i].setFixedWidth(80)
            buttons[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            options_layout.addWidget(buttons[i])
            if i % 2 == 0 and i != len(buttons) - 1:
                options_layout.addStretch()

        return options_layout

    def update_image(self, data):
        """
        Updates the image of the webcam video.

        :param data: The image data (image, height of the image, width of the image).
        """

        image, image_height, image_width = data
        image = QtGui.QImage(image.data, image_width, image_height, QtGui.QImage.Format.Format_RGB888).scaled(
            self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        self.video.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        """
        Closes the application.

        :param event: The close event when the user clicks on the close button.
        """

        self.thread.stop()
        settings.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = SettingsWindow()
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
