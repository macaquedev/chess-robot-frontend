import serial


class Arduino:
    def __init__(self, port="/dev/ttyUSB0", baud_rate=115200):
        while True:
            try:
                self.arduino = serial.Serial(port, baud_rate)
            except Exception as e:
                print(e)
                continue
            break

        self.wait_for_acknowledgement()
        self.send_acknowledgement()

    def data_waiting(self):
        return self.arduino.inWaiting()

    def get_data(self):
        return self.arduino.readline().decode("utf-8").strip()

    def send_data(self, d):
        self.arduino.write((d + "\r").encode())

    def send_data_and_wait_for_acknowledgement(self, d):
        self.send_data(d)
        self.wait_for_acknowledgement()

    def wait_for_acknowledgement(self):
        while True:
            if self.data_waiting():
                if self.get_data() == "OK":
                    return

    def received_acknowledgement(self):
        if self.data_waiting():
            a = self.get_data()
            if a == "OK":
                return True
        return False

    def send_acknowledgement(self):
        self.send_data("OK")
