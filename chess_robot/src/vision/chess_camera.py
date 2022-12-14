import cv2
import pickle
from chess_robot.src.vision import transform
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
import os


class ChessCamera:
    def __init__(self, camera_index):
        self.cap = WebcamVideoStream(src=camera_index).start()
        try:
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "points.pickle"), "rb") as f:
                self.points, self.rotation_degree = pickle.load(f)
                self.points = np.array(self.points)
        except Exception as _:
            print("Please calibrate the camera before starting it")
            self.cap.stop()
            exit(-1)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cap.stop()

    def read(self):
        frame = self.cap.read()
        warped_image = transform.four_point_transform(frame, self.points)
        rotated_image = imutils.rotate_bound(warped_image, self.rotation_degree)
        return cv2.resize(rotated_image, (400, 400))

    @staticmethod
    def draw_lines(f):
        frame = f.copy()
        for i in range(1, 8):
            mx_pt = int((i / 8.0) * 400)
            cv2.line(frame, (0, mx_pt), (400, mx_pt), (0, 0, 255))
            cv2.line(frame, (mx_pt, 0), (mx_pt, 400), (0, 0, 255))

        return frame
