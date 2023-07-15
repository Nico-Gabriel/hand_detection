# Hand Detection

Python hand detection using OpenCV and MediaPipe, implemented in a virtual drawing board application.

Author: **Nico-Gabriel Ruckendorfer**

---

## Install dependencies

> **Note:** This project was developed using Python 3.10. It is recommended to use the same version or a newer one.

For this project, you will need to install the following dependencies:

- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [PyQt6](https://pypi.org/project/PyQt6/)

### OpenCV

```bash
pip install opencv-python
```

### MediaPipe

```bash
pip install mediapipe
```

_or on **Apple Silicon**_

```bash
pip install mediapipe-silicon
```

### PyQt6

```bash
pip install PyQt6
```

---

## Information

> **Note:** For this project, you will need a webcam, either a built-in or an external one.

### OpenCV

![OpenCV logo](assets/opencv.png)

In this project, OpenCV is used to capture the video stream from the webcam and for image manipulation to draw the
lines and the indicator (which is needed to see where the line will be drawn) on the current frame, which are then 
displayed on a white layer in the virtual drawing board application.

Links:

- [Capturing video in OpenCV](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
- [Drawing lines in OpenCV](https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html)

For more information about OpenCV, visit the [official website](https://opencv.org/).

### MediaPipe

![MediaPipe logo](assets/mediapipe.png)

In this project, MediaPipe is used to detect the hand landmarks, wich are needed to get the position of the index 
fingertip and thumb tip to draw.

Links:

- [Hand landmarks in MediaPipe](https://google.github.io/mediapipe/solutions/hands.html)

For more information about MediaPipe, visit the [official website](https://mediapipe.dev/).


## License

This project is free software and may be redistributed under the [MIT-LICENSE](LICENSE).
