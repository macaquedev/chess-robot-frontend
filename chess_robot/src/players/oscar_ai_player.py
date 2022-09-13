from .automated_player import AutomatedPlayer
from . import oscar_ai
import chess


class OscarAIPlayer(AutomatedPlayer):
    def get_move(self):
        oscar_ai.turn = 'B' if self.board.turn == 'W' else 'W'

        if self.board.move_stack:
            oscar_ai.move(self.board.move_stack[-1].uci())

        oscar_ai.turn = 'W' if self.board.turn else 'B'
        move = oscar_ai.minimaxRoot(oscar_ai.depth, oscar_ai.turn)
        print(move)
        oscar_ai.move(move)
        move = chess.Move.from_uci(move)
        return move, self.board.san(move)

