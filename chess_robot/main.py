import time
from chess_robot.config import config
from chess_robot.src.communication.arduino import Arduino
from chess_robot.src.players.human_player import HumanPlayer
from chess_robot.src.players.stockfish_player import StockfishPlayer
from chess_robot.src.players.lichess_opponent import LichessOpponent
from chess_robot.src.players.lichess_game import LichessGame
from chess_robot.src.players.game import Game, transcribe_outcome
from chess_robot.src.vision.chess_camera import ChessCamera

if __name__ == "__main__":
    print("Connecting to chess robot....")
    arduino = Arduino(config.ARDUINO_PORT, config.ARDUINO_BAUDRATE)
    print("Connected to chess robot!")
    time.sleep(1)
    with ChessCamera(config.CAMERA_INDEX) as camera:
        while True:
            while not arduino.data_waiting():
                pass

            data = arduino.get_data()
            if data.startswith("STOCKFISH "):
                data = data[10:].split()
                if data[1] == "1":
                    players = [HumanPlayer(), StockfishPlayer(int(data[0]))]
                else:
                    players = [StockfishPlayer(int(data[0])), HumanPlayer()]
                with Game(*players).attach_arduino(arduino).attach_camera(camera) as g:
                    outcome = g.play()

                print(x := transcribe_outcome(outcome))
                arduino.send_data_and_wait_for_acknowledgement(f"__.{x}")
                arduino.wait_for_acknowledgement()
            elif data.startswith("LICHESS"):
                arduino.send_data_and_wait_for_acknowledgement(f".Connecting to Lichess\nPlease start a game\non your PC")
                with LichessGame(HumanPlayer(), LichessOpponent()).attach_arduino(arduino).attach_camera(camera) as g:
                    outcome = g.play()

                print(x := transcribe_outcome(outcome))
                arduino.send_data_and_wait_for_acknowledgement(f"__.{x}")
