from chessboard import display
import chess
from chess_robot.src.vision.prediction_engine import ChessPieceClassifier
from chess_robot.config import config
import cv2


def transcribe_outcome(outcome):
    if outcome.winner is None:
        outcome = outcome.termination
        if outcome == 2:
            message = "Draw by Stalemate!"
        elif outcome == 3:
            message = "Draw by insufficient material!"
        elif outcome == 4:
            message = "Draw by 75 moves!"
        elif outcome == 5:
            message = "Draw by fivefold repetition!"
        elif outcome == 6:
            message = "Draw by 50 moves!"
        elif outcome == 7:
            message = "Draw by threefold repetition!"
        else:
            message = "Draw!"
    else:
        message = f"{'White' if outcome.winner else 'Black'} won!"

    return message


class Game:
    def __init__(self, white, black):
        self.board = chess.Board()
        self.gameboard = display.start(self.board.fen())
        self.classifier = ChessPieceClassifier()
        self.white = white.attach_parameters(self.gameboard, self.board, self.classifier)
        self.black = black.attach_parameters(self.gameboard, self.board, self.classifier)

    def attach_arduino(self, arduino):
        self.white.attach_arduino(arduino)
        self.black.attach_arduino(arduino)
        return self

    def attach_camera(self, camera):
        self.white.attach_camera(camera)
        self.black.attach_camera(camera)
        return self

    def __enter__(self):
        return self

    def play(self):
        self.white.reset_to_starting_position()
        while not self.board.is_game_over():
            if self.board.turn:
                self.white.play_move()
            else:
                self.black.play_move()

        return self.board.outcome()

    def __exit__(self, *_):
        cv2.destroyAllWindows()
