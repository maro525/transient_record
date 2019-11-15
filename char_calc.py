
class CharCalculatior:

    def __init__(self):
        self.bitlen = 8

    def get_colum_bitdata(self, bit_list, index):
        msg = bit_list[index*self.bitlen: index*self.bitlen+(self.bitlen-1)]
        return msg

    def get_move_data(self, sentence_bit_data, roundtimes):
        split_datas = []
        for c in sentence_bit_data:
            split_data = self.split_bit_data(c, roundtimes)
            split_datas += split_data
        move_data = []
        char_num = len(sentence_bit_data)
        for t in range(roundtimes):
            for i in range(char_num):
                direction = int(not(bool(t%2)))
                sd = split_datas[i][t]
                md = self.make_move_data(sd, direction)
                move_data += md
        return move_data

    def split_bit_data(self, bit_data, num):
        square = self.bitlen * self.bitlen
        splited = [[0]*square] * num
        indx = 0
        for i, b in enumerate(bit_data):
            if b is "1":
                splited[indx][i] = 1
                indx += 1
                if indx is 4:
                    indx = 0
        return splited

    def make_move_data(self, split_data, direction):
        mds = []
        for i in range(self.bitlen):
            md = []
            tmp = self.get_colum_bitdata(split_data, i)
            md += tmp
            md += direction
            mds.append(md)
        return mds

    def int2str(self, int_list):
        s = ""
        for i in int_list:
            if i is 1:
                s.append("1")
            elif i is 0:
                s.append("0")
        return s
