from chess_robot.src.vision.chess_camera import ChessCamera
from chess_robot.config import config

import cv2

if __name__ == "__main__":
    with ChessCamera(config.CAMERA_INDEX) as cam:
        while True:
            img = cam.read()
            cv2.imshow("Chess Camera", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
