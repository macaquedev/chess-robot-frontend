import pickle
import random
import cv2
import os

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA

from chess_robot.config import config

import chess


def get_move_from_prediction(board, prediction, current_position):
    differences = []
    for i in range(8):
        for j in range(8):
            if prediction[i][j] != current_position[i][j]:
                differences.append([i, j, prediction[i][j], current_position[i][j]])
    if len(differences) == 0:
        return None, "No move made, \nplease try again", (None, None)

    elif len(differences) == 1:
        new_colour, old_colour = differences[0][2], differences[0][3]
        if old_colour == 2:
            return None, (
                f"""A piece appeared \non {
                chess.square_name(chess.square(differences[0][1], 7 - differences[0][0]))
                }. \nPlease remove it."""), (None, None)
        elif new_colour == 2:
            return None, (
                f"""A piece disappeared \non {
                chess.square_name(chess.square(differences[0][1], 7 - differences[0][0]))
                }. \nPlease replace it."""), (None, None)
        elif new_colour == 1:
            return None, (
                f"""A piece turned from \nblack to white on {
                chess.square_name(chess.square(differences[0][1], 7 - differences[0][0]))
                }. \nPlease adjust it."""), (None, None)
        else:
            return None, (
                f"""A piece turned from \nwhite to black on {
                chess.square_name(chess.square(differences[0][1], 7 - differences[0][0]))
                }. \nPlease adjust it."""), [None, None]

    elif len(differences) == 2:  # Move or capture
        if differences[0][2] == differences[1][3] and differences[0][3] == differences[1][2]:  # Move
            starting_coordinate = [differences[1][1], 7 - differences[1][0]]
            ending_coordinate = [differences[0][1], 7 - differences[0][0]]
            piece_colour = differences[0][2]
            if piece_colour == 2:
                starting_coordinate, ending_coordinate = ending_coordinate, starting_coordinate
                piece_colour = differences[1][2]
        else:
            if {differences[0][2], differences[0][3]} == {0, 1}:  # differences[0] changed colour, so capture
                starting_coordinate = [differences[1][1], 7 - differences[1][0]]
                ending_coordinate = [differences[0][1], 7 - differences[0][0]]
                moves_set = {differences[1][2], differences[1][3]}
            else:
                starting_coordinate = [differences[0][1], 7 - differences[0][0]]
                ending_coordinate = [differences[1][1], 7 - differences[1][0]]
                moves_set = {differences[0][2], differences[0][3]}
            if 2 not in moves_set:  # somehow 2 pieces switched colours?
                return None, "Illegal move, \nplease try again", (None, None)

            moves_set.remove(2)
            piece_colour = moves_set.pop()

        if piece_colour != board.turn:
            return None, "Move out of turn! \nPlease try again.", (None, None)

        try:
            move = board.find_move(chess.square(*starting_coordinate), chess.square(*ending_coordinate))
        except ValueError as _:
            return None, "Illegal move, \nplease try again.", (None, None)

        if board.is_en_passant(move):
            to_be_removed = [ending_coordinate[0], ending_coordinate[1] - (1 if board.turn else -1)]
            return move, None, (to_be_removed, None)

        elif board.is_castling(move):
            if board.is_kingside_castling(move):
                rook_positions = ("h1", "f1") if board.turn else ("h8", "f8")
            else:
                rook_positions = ("a1", "d1") if board.turn else ("a8", "d8")
            return move, None, (None, rook_positions)

        return move, None, (None, None)

    else:  # castling or en passant, also possibly a misdetection or illegal move.
        if len(differences) == 3:  # en passant?
            for i in range(3):
                if differences[i][2] == 2 and differences[i][3] != int(
                        board.turn):  # the piece that is being captured is removed.
                    break
            else:
                return None, "Invalid move, \nplease try again", (None, None)

            differences.pop(i)
            starting_coordinate = [differences[1][1], 7 - differences[1][0]]
            ending_coordinate = [differences[0][1], 7 - differences[0][0]]
            if differences[0][2] == 2:
                starting_coordinate, ending_coordinate = ending_coordinate, starting_coordinate

            try:
                move = board.find_move(chess.square(*starting_coordinate), chess.square(*ending_coordinate))
            except ValueError:
                return None, (
                    f"""Cannot perform en passant\nfrom {
                    chess.square_name(chess.square(*starting_coordinate))} to {
                    chess.square_name(chess.square(*ending_coordinate))
                    },\nplease try again."""), (None, None)

            return move, None, (None, None)

        elif len(differences) == 4:  # castling?
            if board.turn:
                squares_involved_in_castling = [[0, 2, 3, 4], [4, 5, 6, 7]]  # [queenside, kingside]
            else:
                squares_involved_in_castling = [[56, 58, 59, 60], [60, 61, 62, 63]]  # [queenside, kingside]

            differences.sort(key=lambda x: chess.square(x[1], 7 - x[0]))
            squares_involved_in_move = [chess.square(i[1], 7 - i[0]) for i in differences]
            if squares_involved_in_move in squares_involved_in_castling:  # castling successful
                if not (differences[1][2] == differences[2][2] == board.turn
                        and differences[0][2] == differences[3][2] == 2):
                    return None, "Invalid castling. \nPlease try again.", (None, None)
                starting_coordinate = 4 if board.turn else 60
                if squares_involved_in_move == squares_involved_in_castling[0]:  # queenside?
                    if not board.has_queenside_castling_rights(board.turn):
                        return None, "Cannot castle queenside. \nPlease make another move.", (None, None)
                    ending_coordinate = 2 if board.turn else 58
                else:
                    if not board.has_kingside_castling_rights(board.turn):
                        return None, "Cannot castle kingside. \nPlease make another move.", (None, None)
                    ending_coordinate = 6 if board.turn else 62
                try:
                    move = board.find_move(starting_coordinate, ending_coordinate)

                except ValueError:
                    return None, (
                        f"""Cannot castle from {
                        chess.square_name(starting_coordinate)} \nto {
                        chess.square_name(ending_coordinate)}, please try again."""), (None, None)

                return move, None, (None, None)

            else:
                return None, "Invalid move. \nPlease try again", (None, None)
        else:
            return None, "Invalid move. \nPlease try again", (None, None)


class ChessPieceClassifier:
    def __init__(self):
        try:
            with open(config.MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(config.PCA_PATH, "rb") as f:
                self.pca = pickle.load(f)

        except FileNotFoundError:
            with open(
                    os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "model", 'data.pickle'),
                    'rb') as f:
                data = pickle.load(f)
            random.shuffle(data)
            features = []
            labels = []

            for feature, label in data:
                features.append(feature)
                labels.append(label)

            x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

            self.pca = PCA(n_components=16, whiten=True)
            self.pca.fit(x_train)
            x_train_pca = self.pca.transform(x_train)
            x_test_pca = self.pca.transform(x_test)

            self.model = SVC(C=0.5)
            self.model.fit(x_train_pca, y_train)

            prediction = self.model.predict(x_test_pca)
            accuracy = accuracy_score(prediction, y_test)

            print(f"Accuracy: {accuracy * 100}%")

            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "model", "model.sav"),
                      "wb") as f:
                pickle.dump(self.model, f)
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "model", "model.pca"),
                      "wb") as f:
                pickle.dump(self.pca, f)

        self.labels = ["black", "white", "empty"]
        self.chessboard = cv2.resize(
            cv2.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)), "chessboard.png")),
            (400, 400))

    def predict(self, img):
        prediction = [[0 for _ in range(8)] for _ in range(8)]
        for m, i in enumerate(range(0, img.shape[0], 50)):
            for n, j in enumerate(range(0, img.shape[1], 50)):
                roi = img[i:i + 50, j:j + 50, :].copy()
                roi = cv2.addWeighted(roi, config.CONTRAST_FACTOR, roi, 0, config.BRIGHTNESS_FACTOR)
                roi = roi // 4 * 4 + 4 // 2
                img[i:i + 50, j:j + 50, :] = roi
                p = self.model.predict(self.pca.transform(np.array([roi.flatten()])))
                prediction[m][n] = p[0]

        output_image = self.chessboard.copy()
        for m, i in enumerate(range(0, output_image.shape[0], 50)):
            for n, j in enumerate(range(0, output_image.shape[1], 50)):
                if prediction[m][n] == 0:
                    cv2.circle(output_image, (j + 25, i + 25), 10, (0, 30, 59), -1)
                elif prediction[m][n] == 1:
                    cv2.circle(output_image, (j + 25, i + 25), 10, (200, 235, 235), -1)

        return prediction, output_image
