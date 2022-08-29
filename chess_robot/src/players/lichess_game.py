import berserk
from .game import Game
from chess_robot.config import config


class LichessGame(Game):
    def __init__(self, human, opponent):
        self.session = berserk.TokenSession(config.LICHESS_API_TOKEN)
        self.client = berserk.Client(session=self.session)
        while len(self.client.games.get_ongoing()) == 0:
            pass
        self.game = self.client.games.get_ongoing()[0]
        if self.game["color"] == "white":
            super().__init__(human, opponent)
        else:
            super().__init__(opponent, human)
        self.white.client = self.black.client = self.client
        self.white.game_id = self.black.game_id = self.game["gameId"]
        self.white.stream = self.black.stream = self.stream = self.client.board.stream_game_state(self.game["gameId"])

    def play(self):
        self.white.arduino.send_data_and_wait_for_acknowledgement("1" if self.game["color"] == "white" else "0")
        super().play()
