from com_manager import Plotter_Manager, Pomp_Manager 
from util import Char_Getter
import time

class Char_Controller:
    def __init__(self):
        self.char_getter = Char_Getter()
        # self.plotter = Plotter_Manager()
        # self.pomp = Pomp_Manager()

    def write_char(self, c):
        array = self.char_getter.get_charArray(c)
        for i in range(8):
            print("Char:{} - Array:{}".format(c, i))
            self.plotter.update()
            self.plotter.move()
            msg = array[i*8: i*8+7]
            self.pomp.handle(msg)
        print("Wrote", c)

    def write_sentence(self, s):
        for c in s:
            self.write_char(c)

    def close(self):
        self.pomp.close()
        self.plotter.close()



class Transient_Record:
    def __init__(self):
        self.cc = Char_Controller()

    def main(self, sentence):
        self.cc.write_sentence(sentence)

    def char_check(self, c):
        # self.pomp_check(9, 1)
        self.cc.write_char(c)
        self.plotter_move(0, 8)

    def plotter_move(self, dir, times):
        self.cc.plotter.test(dir, times)

    def pomp_check(self, v, times):
        for i in range(times):
            self.cc.pomp.test(v)

    def all_check(self, v, times):
        for i in range(times):
            self.cc.pomp.test(v)
            self.cc.plotter.test(1, 1)
        self.plotter_move(0, times)

    def finish(self):
        self.cc.close()

tr = Transient_Record()

# tr.main("Good Morning") # 文章を書く
tr.char_check("あ") # 文字チェク。 一文字かく
# tr.plotter_move(1, 10) # 例 : (1,8)と設定したら、正転×8. (0,8)と設定したら、逆転×8
# tr.pomp_check(9, 10) # n番目のポンプをON 。 0にしたときは全部OFF 9は全部ON, それを×n回
# tr.all_check(2, 10)

# for i in range(50):
    # tr.char_check("B")

tr.finish()