from .automated_player import AutomatedPlayer
from stockfish import Stockfish
import chess


class StockfishPlayer(AutomatedPlayer):
    def __init__(self, strength):
        super().__init__()
        self.stockfish = Stockfish()
        self.stockfish.set_elo_rating(strength)

    def get_move(self):
        self.stockfish.set_fen_position(self.board.fen())
        notation = self.board.san(move := chess.Move.from_uci(self.stockfish.get_best_move()))
        return move, notation

