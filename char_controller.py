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
        for c in chars:
            self.written_chars += 1
            self.write_char(c)
            if self.plotter.breaknum > 4:
                self.init_new()

    def init_new(self):
        self.plotter.close()
        self.plotter = None
        self.plotter = Plotter_Manager()
        self.plotter.breaknum =0

    def write_char(self, c):
        print("Write Char", c)
        try:
            array = self.char_getter.get_charArray(c)
        except:
            print("urllib error........................")
        for i in range(8):
            print("Char:{} - Array:{}".format(c, i))
            self.plotter.move(0)
            msg = self.cc.get_colum_bitdata(array, i)
            self.pomp.handle(msg)
        print("Wrote", c)


    def close(self):
        self.pomp.close()
        self.plotter.close()
