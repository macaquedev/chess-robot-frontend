import imutils
import cv2
import numpy as np
from chess_robot.src.vision import transform
import pickle
from imutils.video import WebcamVideoStream
import os
from chess_robot.config import config

window_width = 640
window_height = 480
flip = 2

cam = WebcamVideoStream(config.CAMERA_INDEX).start()


def calibrate_camera():
    while True:
        try:
            frame = cam.read()
            draw_frame = frame.copy()

            hsv = cv2.cvtColor(draw_frame, cv2.COLOR_BGR2HSV)

            red_foreground_mask_1 = cv2.inRange(hsv, np.array([155, 125, 125]), np.array([179, 255, 255]))
            red_foreground_mask_2 = cv2.inRange(hsv, np.array([0, 125, 125]), np.array([10, 255, 255]))
            red_foreground_mask = cv2.add(red_foreground_mask_1, red_foreground_mask_2)

            green_foreground_mask = cv2.inRange(hsv, np.array([60, 100, 140]), np.array([120, 255, 255]))

            red_contours, _ = cv2.findContours(red_foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            green_contours, _ = cv2.findContours(green_foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            count = 0
            centroids = []
            rectangles = []
            for cnt in red_contours:
                area = cv2.contourArea(cnt)
                if area >= 250:
                    count += 1
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    rectangles.append([(x, y), (x + w, y), (x, y + h), (x + w, y + h)])
                    centroids.append([x + (w // 2), y + (h // 2)])
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

            (x, y, w, h) = cv2.boundingRect(max(green_contours, key=cv2.contourArea))
            cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            rectangles.append([(x, y), (x + w, y), (x, y + h), (x + w, y + h)])
            centroids.append(green_point := [x + (w // 2), y + (h // 2)])

            sorted_points = transform.order_points(np.array(centroids)).tolist()
            indexes = [sorted_points.index(i) for i in centroids]
            rectangles = [rectangles[i] for i in indexes]
            current_green_point_index = 0
            for index, point in enumerate(sorted_points):
                cv2.circle(draw_frame, (int(point[0]), int(point[1])), 5, (25, 0, 0), 2)
                cv2.putText(draw_frame, str(index), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0), 2)
                if point == green_point:
                    current_green_point_index = index
            rotation_degree = 90 * (3 - current_green_point_index)

            inner_points = [min(i, key=lambda p: abs((window_width // 2 - p[0]) ** 2 + (window_height // 2 - p[1]) ** 2))
                            for i in
                            rectangles]

            warped_image = transform.four_point_transform(frame, np.array(inner_points))

            for point in inner_points:
                cv2.circle(draw_frame, (int(point[0]), int(point[1])), 5, (25, 0, 0), 2)

            rotated_image = imutils.rotate_bound(warped_image, rotation_degree)
            rotated_image = cv2.resize(rotated_image, (400, 400))

            for i in range(1, 8):
                mx_pt = int((i / 8.0) * 400)
                cv2.line(rotated_image, (0, mx_pt), (400, mx_pt), (0, 0, 255))
                cv2.line(rotated_image, (mx_pt, 0), (mx_pt, 400), (0, 0, 255))
            cv2.imshow('Chessboard', draw_frame)
            cv2.moveWindow('Chessboard', 0, 0)
            cv2.imshow('New', rotated_image)
            if k := cv2.waitKey(1) == ord('k'):
                with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "src", "vision",
                                       "points.pickle"), "wb") as f:
                    pickle.dump([inner_points, rotation_degree], f)
                return
            elif k == ord('q'):
                return

        except (ValueError, IndexError):
            try:
                cv2.imshow('Chessboard', draw_frame)
                if k := cv2.waitKey(1) == ord('k'):
                    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "src", "vision",
                                           "points.pickle"), "wb") as f:
                        pickle.dump([inner_points, rotation_degree], f)
                    return
                elif k == ord('q'):
                    return
            except NameError as _:
                return



if __name__ == "__main__":
    calibrate_camera()
    cam.stop()
    cv2.destroyAllWindows()