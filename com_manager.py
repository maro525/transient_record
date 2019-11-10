from util import Serial_Controller

PORT_POMP = "COM6"
PORT_PLOTTER = "COM7"
BAUDRATE = 38400


class Plotter_Manager:
    def __init__(self):
        self.max_len = 10
        self.plotter_pos = 0
        self.dir = 1
        self.plotter_serial = Serial_Controller(PORT_PLOTTER, BAUDRATE)

    # update plotter direction
    def update(self):
        if self.dir is 1:
            self.plotter_pos += 1
            if self.plotter_pos > self.max_len:
                self.plotter_pos = self.max_len
                self.dir = 0
        elif self.dir is 0:
            self.plotter_pos -= 1
            if self.plotter_pos < 10:
                self.plotter_pos = 0
                self.dir = 1

    def move(self):
        if self.dir is 1:
            self.plotter_serial.send_msg(b"a.")
        elif self.dir is 0:
            self.plotter_serial.send_msg(b"b.")
        elif self.dir is -1:
            self.plotter_serial.send_msg(b"h.")
        rep = ""
        while True:
            rep = self.plotter_serial.read_reply()
            if rep == "Done.":
                break
        # print("plotter move succeeded")
    
    def test(self, dir, times):
        self.dir = dir
        for i in range(times):
            self.move()

    def close(self):
        self.plotter_serial.close()


class Pomp_Manager:
    def __init__(self):
        self.pomp_serial = Serial_Controller(PORT_POMP, BAUDRATE)

    def handle(self, msg):
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
            sig = ""
            for i in range(v):
                sig += "0"
            sig += "1"
            for i in range(8-v+1):
                sig += "0"
        self.handle(msg)
        

    def close(self):
        self.pomp_serial.close()

