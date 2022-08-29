from chess_robot.src.vision.chess_camera import ChessCamera
from chess_robot.src.vision.prediction_engine import ChessPieceClassifier
from chess_robot.config import config
import argparse
import cv2
import os


if __name__ == "__main__":
    c = ChessPieceClassifier()
    with ChessCamera(config.CAMERA_INDEX) as cam:
        while True:
            frame = cam.read() #  cv2.imread("/home/alex/Python/chess-robot/data2/1/0/1661364750.jpg") #cam.read()
            prediction, output_image = c.predict(frame)
            print(prediction)
            cv2.imshow("F", frame)
            cv2.imshow("P", output_image)

            while True:
                k = cv2.waitKey(1) & 0xFF
                if k in [ord('q'), ord('k')]:
                    break

            if k == ord('q'):
                break

    cv2.destroyAllWindows()
