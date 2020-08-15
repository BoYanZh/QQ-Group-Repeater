import jieba
import json
from pypinyin import lazy_pinyin


class EmojiHelper:
    def __init__(self, path="./data/emoji.json"):
        super().__init__()
        self.emojiDict = json.load(open(path, mode="r", encoding="utf8"))
        self.pinyinDict = {
            ''.join(lazy_pinyin(text)): emoji
            for text, emoji in self.emojiDict.items()
        }
        self.pinyinDict = {}
        for text, emoji in self.emojiDict.items():
            py = ''.join(lazy_pinyin(text))
            self.pinyinDict[py] = emoji

    def transform(self, text, isDeepMode=False):
        textJieba = jieba.cut(text, cut_all=False)
        reList = []
        for word in textJieba:
            word = word.strip()
            if word in self.emojiDict.keys():
                re = self.emojiDict[word]
                reList.append([word, re])
            else:
                if len(word) > 0:
                    for character in word:
                        if character in self.emojiDict.keys():
                            re = self.emojiDict[character]
                            reList.append([character, re])
                        else:
                            reList.append([character, character])
                else:
                    reList.append([word, word])
        if not isDeepMode:
            return "".join([s[1] for s in reList])
        for i in range(len(reList)):
            ori, new = reList[i]
            if ori != new:
                continue
            pinyin = ''.join(lazy_pinyin(reList[i][0]))
            if pinyin in self.pinyinDict.keys():
                re = self.pinyinDict[pinyin]
                reList[i][1] = re
            else:
                reList[i][1] = reList[i][0]
        return "".join([s[1] for s in reList])


if __name__ == "__main__":
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    re = EmojiHelper("../data/emoji.json").transform("叶宝是震惊长安第一拳",
                                                     isDeepMode=True)
    print(re)