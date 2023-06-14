"""
MediaPipe Hands

This example shows how to detect hands and their landmarks from a webcam input.

It is required that 'opencv-python' and 'mediapipe' are installed.

Documentation: https://google.github.io/mediapipe/solutions/hands
"""

import cv2
import mediapipe as mp

KEYCODE_ESC = 27

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
video = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:
    while video.isOpened():

        _, image = video.read()  # get the current frame from the webcam
        results = hands.process(image).multi_hand_landmarks  # get the hand landmarks from the current frame

        if results:
            # draw the hand annotations on the image
            for hand_landmarks in results:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # flip the image horizontally for a selfie-view display and show it
        cv2.imshow("Hand detection", cv2.flip(image, 1))

        # terminate if the escape key is pressed
        if cv2.waitKey(1) == KEYCODE_ESC:
            break

video.release()
