import serial
import time
import urllib.request

class Serial_Controller:
    def __init__(self, port, baudrate):
        print("Serial Connecting...")
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def send_msg(self, msg):
        self.ser.write(msg)
        print("send ", msg)

    def read_reply(self):
        reply = self.ser.readline()
        reply = reply.decode()
        reply = reply.rstrip("\n")
        reply = reply.rstrip("\r")
        print("recv ", reply)
        return reply
    
    def close(self):
        self.ser.close()

class Char_Getter:
    def __init__(self):
        self.url = "https://arcane-bayou-55620.herokuapp.com/getArray/"

    def get_charArray(self, c):
        url = self.url + c
        array = urllib.request.urlopen(url).read()
        a = array.decode()
        return a

    # TODO
    def reshape(self, a):
        b = ""
        for i in range(8):
            for j in range(8):
                tmp = a[i*8+j]