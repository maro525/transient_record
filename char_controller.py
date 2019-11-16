from util import Char_Getter
from com_manager import Plotter_Manager, Pomp_Manager
from char_calc import CharCalculatior

class Char_Controller:
    def __init__(self):
        self.char_getter = Char_Getter()
        self.plotter = Plotter_Manager()
        self.pomp = Pomp_Manager()
        self.cc = CharCalculatior()
        self.written_chars = 0
        self.bError = False

    def write_sentence(self, sentence, roundtimes):
        print("Write Sentence", sentence)
        self.written_chars = 0
        if roundtimes is 1:
            self.write_chars(sentence)
            return
        else:
            sentence_bit_data = self.get_array_data(sentence)
            move_data = self.cc.get_move_data(sentence_bit_data, roundtimes)
            for i in range(len(move_data)):
                direction = move_data[i][8]
                self.plotter.move(direction)
                bit_data = move_data[i][0:8]
                msg = self.cc.int2str(bit_data)
                self.pomp.handle(msg)


    def get_array_data(self,sentence):
        sentence_bit_data = []
        for c in sentence:
            a = self.char_getter.get_charArray(c)
            sentence_bit_data.append(a)
        return sentence_bit_data

    def write_chars(self, chars):
        for ind, c in enumerate(chars):
            print("char")
            self.init_new()
            if ind is 5:
                print("this is char6. write partply")
                self.write_char_part(c, 6)
            else:
                self.write_char(c)

    def init_new(self):
        if self.plotter.breaknum > 4:
            self.plotter.close()
            self.plotter = None
            self.plotter = Plotter_Manager()
            self.plotter.breaknum =0

    def write_char(self, c):
        print("Write Char", c)
        try:
            a = self.char_getter.get_charArray(c)
            print(a)
        except:
            print("urllib error........................")
            self.bError = True
            return
        for i in range(8):
            print("Char:{} - Array:{}".format(c, i))
            self.plotter.move(0)
            msg = self.cc.get_colum_bitdata(a, i)
            self.pomp.handle(msg)
            self.init_new()
        print("Wrote", c)

    def write_char_part(self, c, p):
        print("Write Char Part", c)
        try:
            a = self.char_getter.get_charArray(c)
        except:
            self.bError = True
            print("urllib error........................")
            return
        for i in range(p):
            print("Char:{} - Array:{}".format(c, i))
            self.plotter.move(0)
            msg = self.cc.get_colum_bitdata(a, i)
            self.pomp.handle(msg)
            self.init_new()
        print("Wrote", c)

    def close(self):
        self.pomp.close()
        self.plotter.close()
