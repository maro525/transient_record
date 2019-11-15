import time
from trend_getter import TrendGetter
from char_controller import Char_Controller


class Transient_Record:
    def __init__(self):
        self.cc = Char_Controller()
        self.tg = TrendGetter()
        self.resting_duration = 300
        self.round_times = 1
        self.max_char = 6

    def main(self):
        while True:
            sentence = self.tg.get_random_word()
            if len(sentence) > self.max_char:
                print(sentence, end="")
                print(" is too long")
                sentence = sentence[0:self.max_char]
            starttime = time.time()
            self.cc.write_sentence(sentence, self.round_times)
            for i in range(self.cc.written_chars):
                self.plotter_move(1, 8)
                if self.cc.plotter.breaknum > 4:
                    self.cc.init_new()
            print("write", sentence, "Done.")
            # self.get_back_fast(1, 8*self.cc.written_chars)
            # self.sentence_check(sentence)
            duration = time.time() - starttime
            print("duration", duration)
            if duration < self.resting_duration:
                sleeptime = self.resting_duration - duration
                time.sleep(sleeptime)
                print("sleep", sleeptime)

    def sentence_check(self, sentence):
        # self.cc.write_sentence(sentence)
        i = 0
        for c in sentence:
            self.char_check(c)
            i += 1
        for i in range(i):
            self.plotter_move(1, 8)

    def get_back_fast(self, dir, times):
        for i in range(times):
            self.cc.plotter.movefast(1)

    def char_check(self, c):
        # self.pomp_check(9, 1)
        self.cc.write_char(c)
        # self.plotter_move(0, 8)

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


if __name__ == '__main__':
    tr = Transient_Record()

    # tr.main()
    # tr.sentence_check("GOOD DAY")
    # tr.char_check("あ") # 文字チェク。 一文字かく
    # tr.plotter_move(1, 25)
    # tr.plotter_move(1, 4) # 例 : (1,8)と設定したら、正転×8. (0,8)と設定したら、逆転×8
    tr.pomp_check(1, 30) # n番目のポンプをON 。 0にしたときは全部OFF 9は全部ON, それを×n回
    # tr.all_check(2, 10)

    # for i in range(50):
        # tr.char_check("B")

    tr.finish()
