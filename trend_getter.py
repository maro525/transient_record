# -*- coding: utf-8 -*-
import MeCab
import jaconv
import re, regex
from pykakasi import kakasi
from pytrends.request import TrendReq
import pandas, numpy, random, requests


class TrendGetter:
    def __init__(self):
        #MeCab設定
        tagger_neolog = MeCab.Tagger("-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd")
        self.tagger = MeCab.Tagger("-Ochasen")

        #kakasi設定
        kak = kakasi()
        kak.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
        self.conv = kak.getConverter()

        self.p = re.compile('[0-9a-zA-Zあ-んー\u30A1-\u30F4]+')
        self.pytrends = TrendReq(hl='ja-JP', tz=360)
        self.trend_words = ['レコードたい', 'にいがた', 'みずのみき', 'たにぐちゆきひろ', 'ポケモン', 'アナとゆきの', 'やまのてせん', 'ワンパチ', 'いながきけいた', 'いきなりステーキ', 'ハンセンびょう', 'おかむらたかし', 'あさひなお', 'ブラックフライデー', 'りんごちゃん']
        self.demo_index = 0

    def get_words(self):
        trends = self.pytrends.trending_searches(pn='japan')
        trends = trends.values.tolist()

        trendList = []
        for t in trends:
            if self.p.fullmatch(t[0]):
                trendList.append(t[0])
            else:
                #トレンドが正規表現にマッチせず
                ans = ""
                words = []
                result = self.tagger.parse(t[0]).split("\n")
                for res in result:
                    words.append(self.tagger.parse(res).split("\t"))
                for word in words:
                    if len(word) > 1 and word[0] != "EOS":
                        if regex.findall(r'\p{Han}+',word[0]):
                            if not regex.findall(r'\p{Han}+',word[1]):
                                ans += jaconv.kata2hira(word[1])
                            else:
                                ans += self.conv.do(word[1])
                        else:
                            ans += word[0]
                trendList.append(ans)
        return trendList

    def get_random_word_demo(self):
        tw = self.trend_words[self.demo_index]
        self.demo_index += 1
        if demo_index >= len(self.trend_words):
            self.demo_index = 0
        return tw

    def get_random_word(self):
        trends = self.get_words()
        word = random.choice(trends)
        return word

if __name__ == '__main__':
    tg = TrendGetter()
    rw = tg.get_random_word()
    print(rw)