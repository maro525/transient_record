from util import Serial_Controller

PORT_POMP = "/dev/ttyUSB0"
PORT_PLOTTER = "/dev/ttyACM0"
BAUDRATE = 38400


class Plotter_Manager:
    def __init__(self):
        self.plotter_serial = Serial_Controller(PORT_PLOTTER, BAUDRATE)

    def move(self, dir):
        if dir is 1:
            self.plotter_serial.send_msg(b"a.")
        elif dir is 0:
            self.plotter_serial.send_msg(b"b.")
        elif dir is -1:
            self.plotter_serial.send_msg(b"h.")
        rep = ""
        ww = 0
        while True:
            ww += 1
            rep = self.plotter_serial.read_reply()
            if rep == "Done.":
                break
            if ww > 5:
                break
        # print("plotter move succeeded")
    
    def test(self, dir, times):
        for i in range(times):
            print("--- {} / {}".format(i, times))
            self.move(dir)

    def close(self):
        self.plotter_serial.close()


class Pomp_Manager:
    def __init__(self):
        self.pomp_serial = Serial_Controller(PORT_POMP, BAUDRATE)

    def handle(self, msg):
        msg = msg[::-1]
        msg = msg + "n"
        msg = msg.encode()
        self.pomp_serial.send_msg(msg)
        while True:
            rep = self.pomp_serial.read_reply()
            if rep == "Done.":
                break


    def test(self, v):
        if v is 0:
            msg = "00000000"
        elif v is 9:
            msg = "11111111"
        else:
            msg = ""
            for i in range(v-1):
                msg += "0"
            msg += "1"
            for i in range(8-v):
                msg += "0"
        self.handle(msg)
        

    def close(self):
        self.pomp_serial.close()

