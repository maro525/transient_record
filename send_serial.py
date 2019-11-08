import time
import serial

PORT_POMP = "COM7"
PORT_PLOTTER = "COM3"
BAUDRATE = 115200

class Serial_Controller:
    def __init__(self):
        print("Serial Connecting...")
        self.ser_pomp = serial.Serial(PORT_POMP, BAUDRATE, timeout=1)
        self.ser_plotter = serial.Serial(PORT_PLOTTER, BAUDRATE, timeout=1)
        time.sleep(5)

    def read_reply(self):
        print(self.ser_pomp.readline())
        print(self.ser_plotter.readline())

