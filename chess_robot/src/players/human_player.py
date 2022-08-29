import time

from .player import Player
from chess_robot.src.vision.prediction_engine import get_move_from_prediction

import cv2
import chess
from chessboard import display
import string


def fen_to_position(fen):
    output = [[2 for _ in range(8)] for _ in range(8)]
    row = 0
    pointer = 0
    for char in fen:
        if char in string.digits:
            pointer += int(char) - 1

        elif char in string.ascii_lowercase:
            output[row][pointer] = 0
        elif char in string.ascii_uppercase:
            output[row][pointer] = 1
        elif char == "/":
            row += 1
            pointer = -1
        pointer += 1
    return output


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def play_move(self):
        fen = self.board.fen().split()[0]
        position = fen_to_position(fen)
        frame = self.camera.read()
        cv2.imshow('F', frame)
        cv2.waitKey(1)

        predicted_position, output_image = self.classifier.predict(frame)
        cv2.imshow('P', output_image)
        cv2.waitKey(1)

        if predicted_position != position:
            while True:
                self.arduino.send_data("_.Please reset board \nto the correct position.")
                while not self.arduino.received_acknowledgement():
                    frame = self.camera.read()
                    cv2.imshow('F', frame)
                    cv2.waitKey(1)
                predicted_position, output_image = self.classifier.predict(frame)
                cv2.imshow('P', output_image)
                cv2.waitKey(1)
                if predicted_position == position:
                    break
                self.arduino.send_data_and_wait_for_acknowledgement(".Try again.")
                time.sleep(1)
        self.current_position = position[:]
        cv2.imshow('P', output_image)
        cv2.waitKey(1)
        self.arduino.send_data(f"_.{'White' if self.board.turn else 'Black'}, please make a move.")

        while True:
            while not self.arduino.received_acknowledgement():
                frame = self.camera.read()
                cv2.imshow('F', frame)
                cv2.waitKey(1)

            prediction, output_image = self.classifier.predict(frame)
            cv2.imshow('P', output_image)

            move, error, (en_passant_coords, castling_rook_coords) = get_move_from_prediction(
                self.board, prediction, self.current_position)

            if error:
                self.arduino.send_data(f"_.{error}")
                continue

            elif en_passant_coords:
                self.arduino.send_data(
                    f"""_.This move is en passant, \nso please remove the \npawn on {
                    chess.square_name(chess.square(*en_passant_coords))}.""")
                while True:
                    while not self.arduino.received_acknowledgement():
                        frame = self.camera.read()
                        cv2.imshow('F', frame)
                        cv2.waitKey(1)

                    prediction, output_image = self.classifier.predict(frame)
                    cv2.imshow('P', output_image)
                    if prediction[7 - en_passant_coords[1]][en_passant_coords[0]] == 2:
                        break

                    self.arduino.send_data("_.Please try again!")

            elif castling_rook_coords:
                self.arduino.send_data(
                    f"""_.This move is castling, \nso please move the \nrook on {
                    castling_rook_coords[0]} to {castling_rook_coords[1]}.""")

                while True:
                    while not self.arduino.received_acknowledgement():
                        frame = self.camera.read()
                        cv2.imshow('F', frame)
                        cv2.waitKey(1)

                    prediction, output_image = self.classifier.predict(frame)
                    cv2.imshow('P', output_image)
                    starting_rook_position, end_rook_position = [chess.parse_square(i) for i in
                                                                 castling_rook_coords]
                    if prediction[7 - chess.square_rank(starting_rook_position)][
                        chess.square_file(starting_rook_position)] == 2 and prediction[
                        7 - chess.square_rank(end_rook_position)][
                        chess.square_file(end_rook_position)] == self.board.turn:
                        break
                    self.arduino.send_data("_.Please try again!")

            break

        self.arduino.send_data_and_wait_for_acknowledgement(f".OK. {self.board.san(move)}")
        self.board.push(move)
        self.current_position = prediction[:]
        display.update(self.board.fen(), self.gameboard)
        if self.client and self.game_id:
            self.client.board.make_move(self.game_id, move.uci())
            while True:
                event = next(self.stream)
                print(event)
                if event["type"] == "gameState":
                    break
