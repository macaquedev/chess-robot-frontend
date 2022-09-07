import time
import cv2


class Player:
    def __init__(self):
        self.board = None
        self.gameboard = None
        self.camera = None
        self.classifier = None
        self.arduino = None
        self.client = None
        self.game_id = None
        self.stream = None
        self.current_position = [[0] * 8 for _ in range(2)] + [[2] * 8 for _ in range(4)] + [[1] * 8 for _ in range(2)]

    def reset_to_starting_position(self):
        self.arduino.send_data("_.Please reset board \nto the starting position.")
        frame = None
        while True:
            while not self.arduino.received_acknowledgement():
                frame = self.camera.read()
                cv2.imshow('F', self.camera.draw_lines(frame))
                cv2.waitKey(1)
            predicted_position, output_image = self.classifier.predict(frame)
            cv2.imshow('P', output_image)
            cv2.waitKey(1)
            if predicted_position == self.current_position:
                break

            self.arduino.send_data_and_wait_for_acknowledgement(".Try again.")
            time.sleep(1)
            self.arduino.send_data("_.Please reset board \nto the starting position.")

    def attach_parameters(self, gameboard, board, classifier):
        self.gameboard = gameboard
        self.board = board
        self.classifier = classifier
        return self

    def attach_arduino(self, arduino):
        self.arduino = arduino
        return self

    def attach_camera(self, camera):
        self.camera = camera
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def play_move(self):
        pass
