from .player import Player
from chessboard import display
import time
import chess


class AutomatedPlayer(Player):
    def get_move(self):
        return chess.Move(None, None), ""

    def play_move(self):  # data sent to arduino: piece colour, piece type, starting square, ending square, captured piece, gives check, en passant square.
        self.arduino.send_data_and_wait_for_acknowledgement(".Robot's turn...")
        move, notation = self.get_move()
        gives_check = self.board.gives_check(move)
        if self.board.is_queenside_castling(move):
            self.arduino.send_data_and_wait_for_acknowledgement(f"{self.board.turn} C QUEENSIDE CASTLING 0 {gives_check} False")
        elif self.board.is_kingside_castling(move):
            self.arduino.send_data_and_wait_for_acknowledgement(f"{self.board.turn} C KINGSIDE CASTLING 0 {gives_check} False")
        elif self.board.is_en_passant(move):
            ep_square = move.to_square + (-8 if self.board.turn else 8)
            self.arduino.send_data_and_wait_for_acknowledgement(f"{self.board.turn} P {move.from_square} {move.to_square} 0 {gives_check} {ep_square}")
        else:
            piece_type = notation[0] if notation[0] in "NBRQK" else "P"
            if self.board.is_capture(move):
                captured_piece = self.board.piece_at(move.to_square).piece_type
            else:
                captured_piece = 0
            self.arduino.send_data_and_wait_for_acknowledgement(f"{self.board.turn} {piece_type} {move.from_square} {move.to_square} {captured_piece} {gives_check} False")

        self.arduino.send_data_and_wait_for_acknowledgement(f".OK. {notation}")
        self.board.push(move)
        display.update(self.board.fen(), self.gameboard)
        time.sleep(1)
