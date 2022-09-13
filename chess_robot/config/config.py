import os

CONTRAST_FACTOR = 1
BRIGHTNESS_FACTOR = 0
CAMERA_INDEX = 0
MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "model", "model.sav")
PCA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "model", "model.pca")
ARDUINO_PORT = "/dev/ttyUSB0"
ARDUINO_BAUDRATE = 115200
LICHESS_API_TOKEN = "lip_0KjmXCSOjU1xNx02lYgm"
