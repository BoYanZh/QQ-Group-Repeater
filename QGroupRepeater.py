import random
from datetime import datetime, timezone, timedelta
import time
import re
import requests
import json
import os
import logging
import urllib


def load_json(file_name):
    file_path = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], file_name)
    return json.load(open(file_path, 'r', encoding='UTF-8'))


class QGroupBot:
    # settings
    SETTINGS = load_json('settings.json')
    TRASHES = load_json('trash.json')
    NEW_TRASHES = load_json('new_trash.json')
    XM_PR = SETTINGS['XM_PR']
    NOT_XM_PR = SETTINGS['NOT_XM_PR']
    RND_REPEAT_PR = SETTINGS['RND_REPEAT_PR']
    RND_XM_PR = SETTINGS['RND_XM_PR']
    KW_REPEAT_PR = SETTINGS['KW_REPEAT_PR']
    MIN_MSG_INVL = SETTINGS['MIN_MSG_INVL']
    MAX_RND_RE_LEN = SETTINGS['MAX_RND_RE_LEN']
    MAX_RND_XM_LEN = SETTINGS['MAX_RND_XM_LEN']
    SLEEP_TIME = SETTINGS['SLEEP_TIME']
    CLOSE_PR = SETTINGS['CLOSE_PR']
    ADMIN = SETTINGS['ADMIN']
    FIXED_REPLY_DICT = {
        'AT': ['guna，别烦我', '为什么要召唤我？'],
        'LewdDream': ['你  说  话  带  空  格', '唐  突  空  格', '要  素  察  觉'],
        'LewdDream_old': ['你 说 话 带 空 格', '唐 突 空 格', '要 素 察 觉'],
        'Philosophy': [
            'BOY♂NEXT♂DOOR', 'DEEP♂DARK♂FANTASY', 'ASS♂WE♂CAN',
            'Do you like WHAT♂YOU♂SEE', 'SLAVES GET YOUR ASS♂ BACK HERE♂',
            'FA♂Q'
        ]
    }
    REG_REPLY_DICT = {
        r'due|deadline|ddl': ['有你水群的时间，gtt能写2份285作业', '那你怎么还在水群？'],
        r'入学考': ['密院没有入学考哦~（不用考英语）'],
        r'托福': ['''托福要求：
        听力（Listening）：23 
        阅读（Reading）：23 
        口语（Speaking）：21 
        写作（Writing）：21'''],
        r'睡不着': ['唉想睡觉'],
        r'(\S+♂){2,}': [
            'BOY♂NEXT♂DOOR', 'DEEP♂DARK♂FANTASY', 'ASS♂WE♂CAN',
            'Do you like WHAT♂YOU♂SEE', 'SLAVES GET YOUR ASS♂ BACK HERE♂',
            'FA♂Q'
        ]
    }

    def __init__(self, fromGroup):
        self.running = True
        self.fromGroup = fromGroup
        self.mbrArr = [''] * 10
        self.mbrIndex = 0
        self.selfArr = [''] * 10
        self.selfIndex = 0
        self.lastMsgInvl = 10
        self.lastMsgTime = 0
        self.myLastWord = ''
        self.beginTimeStamp = 0
        self.res = ''
        self.msg = ''
        self.context = {}

    def responseMsg(self, context):
        msg = context['message']
        self.context = context
        self.beginTimeStamp = time.time()
        self.res = ''
        # purge msg
        self.msg = msg.strip().strip('\n')
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', self.msg)
        self.msg = re.sub(
            r'/舔|/笑哭|/doge|/泪奔|/无奈|/托腮|/卖萌|/斜眼笑|/喷血|/惊喜|/骚扰|/小纠结|/我最美|/茶|/蛋|/红包|/河蟹|/羊驼|/菊花|/幽灵|/大笑|/不开心|/冷漠|/呃|/好棒|/拜托|/点赞|/无聊|/托脸|/吃|/送花|/害怕|/花痴|/小样儿|/飙泪|/我不看|/啵啵|/糊脸|/拍头|/扯一扯|/舔一舔|/蹭一蹭|/拽炸天|/顶呱呱',
            '', self.msg)
        if (len(self.msg) == 0):
            return ''
        self.getWord()
        self.checkWord()
        return self.res

    # get reply content
    def getWord(self):
        processes = [
            self.replyAT, self.replyFunction, self.checkXM, self.checkKeywords,
            self.checkMeme, self.followRepeat, self.rndRepeat, self.rndXM
        ]
        self.switch()
        if self.running:
            for process in processes:
                process()
                if self.res:
                    break
        return

    # switch on / off of the bot
    def switch(self):
        if (re.search(r'关|停|锤|砸|闭嘴', self.msg) and re.search(r'复读机', self.msg))\
                and not re.search(r'已经|不|开', self.msg):
            if self.running:
                t = datetime.now(timezone(timedelta(hours=8)))
                if self.context['user_id'] % (
                        t.month * 100 + t.day
                ) % 100 < QGroupBot.CLOSE_PR * 100 or self.context[
                        'user_id'] in QGroupBot.ADMIN:
                    self.running = False
                    self.res = '哦，关了'
                else:
                    self.res = '您也配关我？'
        elif (re.search(r'开|启动|修', self.msg) and re.search(r'复读机', self.msg))\
                and not re.search(r'已经|不要', self.msg):
            if not self.running:
                self.running = True
                self.res = '活了'
            else:
                self.res = '你当我是关着的吗？？？'

    # special reply for message starting with '#'
    def replyFunction(self):
        if re.search(r'^#', self.msg):
            tmp_reg = re.search(r'扔(.*)', self.msg)
            if tmp_reg:
                string = tmp_reg.group(1)
                if string in ['骰子', '色子']:
                    self.res = str(random.randint(1, 6))
                elif string in ['硬币']:
                    coin_re = ['正', '反']
                    self.res = coin_re[random.randint(0, 1)]
                elif '复读' in string or 'bot' in string:
                    self.res = '你扔一个试试？'
                elif not string:
                    self.res = '说清楚要扔啥再来问'
                else:
                    tmp_re = QGroupBot.TRASHES.get(string)
                    if tmp_re is not None:
                        self.res = '{}：{}\n'.format(string, tmp_re)
                    tmp_dict = dict()
                    for key, value in QGroupBot.NEW_TRASHES.items():
                        if string in key:
                            tmp_dict[key] = value
                    for key, value in sorted(tmp_dict.items(),
                                             key=lambda d: len(d[0])):
                        self.res += '{}：{}\n'.format(key, value)
                    self.res = self.res.strip('\n')
                    if not self.res:
                        self.res = '扔不来，打扰了'
                    return
            if re.search(r'色图', self.msg):
                imgUrl = self.getUrl()
                if imgUrl:
                    self.res = imgUrl
                else:
                    self.res = '坏了，图没了'

    # reply call
    def replyAT(self):
        if (re.search(r'\[CQ:at,qq={}\]'.format(self.context['self_id']),
                      self.msg)):
            self.res = random.choice(QGroupBot.FIXED_REPLY_DICT['AT'])

    # check XM
    def checkXM(self):
        if (re.search(r'^xm|^羡慕', self.msg)):
            myrand = random.random()
            if (myrand <= QGroupBot.XM_PR):
                if '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '',
                                       self.msg) not in self.selfArr:
                    self.res = self.msg
            elif (myrand >= 1 - QGroupBot.NOT_XM_PR):  # 避免循环羡慕
                if self.msg not in self.selfArr \
                        and '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '', self.msg) not in self.selfArr:
                    self.res = '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '', self.msg)

    # check keywords
    def checkKeywords(self):
        if (re.search(r'tql|nb|ydl|ddw', self.msg)):
            myrand = random.random()
            if (myrand <= QGroupBot.KW_REPEAT_PR):
                self.res = self.msg

    # check meme & regex replys
    def checkMeme(self):
        if (re.search(r'(\S[ ]+){3,}',
                      re.sub(u"[\u4e00-\u9fa5]", 'a', self.msg) + ' ')):
            self.res = random.choice(QGroupBot.FIXED_REPLY_DICT['LewdDream'])
            return
        for regex, words in QGroupBot.REG_REPLY_DICT.items():
            if re.search(regex, self.msg):
                self.res = random.choice(words)
                return

    # followd repeat
    def followRepeat(self):
        if (self.mbrArr.count(self.msg) >= 2):
            self.mbrArr = [''] * 10
            self.res = self.msg
        else:
            self.recordMbrMsg()

    # record previous messages
    def recordMbrMsg(self):
        self.mbrArr[self.mbrIndex] = self.msg
        self.mbrIndex = 0 if self.mbrIndex == 9 else self.mbrIndex + 1
        self.lastMsgInvl += 1
        return

    # random repeat
    def rndRepeat(self):
        if (self.lastMsgInvl > QGroupBot.MIN_MSG_INVL
                and len(self.msg) <= QGroupBot.MAX_RND_RE_LEN):
            myrand = random.random()
            if (myrand <= QGroupBot.RND_REPEAT_PR):
                self.lastMsgInvl = 0
                self.res = self.msg

    # random XM
    def rndXM(self):
        if (len(self.msg) > 2 and not re.search(r'^xm|^羡慕|\?$|？$', self.msg)):
            if (self.lastMsgInvl > QGroupBot.MIN_MSG_INVL
                    and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                myrand = random.random()
                if (myrand <= QGroupBot.RND_XM_PR):
                    self.lastMsgInvl = 0
                    self.msg = re.sub(r'^我的|^我', '', self.msg)
                    self.res = '羡慕' + self.msg

    # avoid repaeting itself / another bot
    def checkWord(self):
        if (self.res == self.msg and self.res in self.selfArr):
            self.res = ''
            return
        else:
            for wordList in QGroupBot.FIXED_REPLY_DICT.values():
                if (self.msg in wordList):
                    self.res = ''
                    return
            self.selfArr[self.selfIndex] = self.res
            self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
            # TODO: rational delay time
            # sleepTimeRemain = (
            #     QGroupBot.SLEEP_TIME if QGroupBot.SLEEP_TIME != 0 else min(
            #         len(self.res) *
            #         0.25, 10)) + self.beginTimeStamp - time.time()
            # if (sleepTimeRemain > 0):
            #     time.sleep(sleepTimeRemain)

    # ???
    def getUrl(self):
        url = "https://yande.re/post.json?limit=1&tags=uncensored&page={}".format(
            random.randint(1, 1000))
        try:
            json = requests.get(url).json()
            return json[0]['file_url']
        except:
            pass
