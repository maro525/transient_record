from util import Char_Getter
from com_manager import Plotter_Manager, Pomp_Manager 
from char_calc import CharCalculatior

class Char_Controller:
    def __init__(self):
        self.char_getter = Char_Getter()
        self.plotter = Plotter_Manager()
        self.pomp = Pomp_Manager()
        self.cc = CharCalculatior()

    def write_sentence(self, sentence, roundtimes):
        print("Write Sentence", sentence)
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


    def write_char(self, c):
        print("Write Char", c)
        array = self.char_getter.get_charArray(c)
        for i in range(8):
            print("Char:{} - Array:{}".format(c, i))
            self.plotter.move(0)
            msg = self.cc.get_colum_bitdata(array, i)
            self.pomp.handle(msg)
        print("Wrote", c)


    def close(self):
        self.pomp.close()
        self.plotter.close()

