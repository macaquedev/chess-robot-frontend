from .automated_player import AutomatedPlayer
import chess


class LichessOpponent(AutomatedPlayer):
    def __init__(self):
        super().__init__()
        self.client = None
        self.has_previously_made_move = False

    def get_from_stream(self):
        return next(self.stream)

    def get_move(self):
        print("getting oppponent move")
        if not self.has_previously_made_move:
            game = self.client.games.get_ongoing()[0]
            if game["lastMove"]:
                last_move = game["lastMove"]
            else:
                while True:
                    event = self.get_from_stream()
                    print(event)
                    if event["type"] == "gameState":
                        break
                last_move = event["moves"].split(' ')[-1]

        else:
            while True:
                event = self.get_from_stream()
                print(event)
                if event["type"] == "gameState":
                    break

            last_move = event["moves"].split(' ')[-1]

        self.has_previously_made_move = True
        return (x := chess.Move.from_uci(last_move)), self.board.san(x)
