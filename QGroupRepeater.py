# -*- coding:gbk -*-
import random
import time
import re
import logging
import json
import os
from urllib2 import Request, urlopen
from urllib import urlencode

class QGroupBot:
    JSON_LOCATION = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'settings.json')
    SETTINGS = json.load(open(JSON_LOCATION))
    XM_PR = SETTINGS['XM_PR']
    NOT_XM_PR = SETTINGS['NOT_XM_PR']
    RND_REPEAT_PR = SETTINGS['RND_REPEAT_PR']
    RND_XM_PR = SETTINGS['RND_XM_PR']
    KW_REPEAT_PR = SETTINGS['KW_REPEAT_PR']
    MIN_MSG_INVL = SETTINGS['MIN_MSG_INVL']
    MAX_RND_RE_LEN = SETTINGS['MAX_RND_RE_LEN']
    MAX_RND_XM_LEN = SETTINGS['MAX_RND_XM_LEN']
    SLEEP_TIME = SETTINGS['SLEEP_TIME']
    FIXED_REPLY_DICT = { \
        'AT': ['guna，别烦我', '为什么要召唤我？'], \
        'LewdDream': ['你  说  话  带  空  格', '唐  突  空  格', '要  素  察  觉'], \
        'LewdDream_old': ['你 说 话 带 空 格', '唐 突 空 格', '要 素 察 觉'], \
        'Philosophy': ['BOY♂NEXT♂DOOR', 'DEEP♂DARK♂FANTASY', 'ASS♂WE♂CAN', 'Do you like WHAT♂YOU♂SEE', 'SLAVES GET YOUR ASS♂ BACK HERE♂', 'FA♂Q'] \
    }

    def __init__(self, fromGroup):
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

        logging.info(os.getcwd())

    def responseMsg(self, msg):
        self.beginTimeStamp = time.time()
        self.res = ''
        #去除首尾空白
        self.msg = msg.strip().strip('\n')
        #去除CQ码图片
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', self.msg)
        #去除非CQ码表情
        self.msg = re.sub(r'/舔|/笑哭|/doge|/泪奔|/无奈|/托腮|/卖萌|/斜眼笑|/喷血|/惊喜|/骚扰|/小纠结|/我最美|/茶|/蛋|/红包|/河蟹|/羊驼|/菊花|/幽灵|/大笑|/不开心|/冷漠|/呃|/好棒|/拜托|/点赞|/无聊|/托脸|/吃|/送花|/害怕|/花痴|/小样儿|/飙泪|/我不看|/啵啵|/糊脸|/拍头|/扯一扯|/舔一舔|/蹭一蹭|/拽炸天|/顶呱呱', '', self.msg)
        if(len(self.msg) == 0):
            return ''
        self.getWord()
        self.checkWord()
        return self.res

    #获取回复内容
    def getWord(self):
        self.replyAT()
        self.checkXM()
        self.checkKeywords()
        self.checkMeme()
        self.followRepeat()
        self.verify()
        self.rndRepeat()
        self.rndXM()
        return

    #回复艾特
    def replyAT(self):
        if(len(self.res) == 0):
            if(re.search(r'\[CQ:at,qq='+QGroupBot.SETTINGS['QQ']+r'\]', self.msg)):
                self.res = random.choice(QGroupBot.FIXED_REPLY_DICT['AT'])
        return

    #羡慕检测
    def checkXM(self):
        if(len(self.res) == 0):
            if(re.search(r'^xm|^羡慕', self.msg)):
                myrand = random.random()
                if(myrand <= QGroupBot.XM_PR):
                    self.res = self.msg
                elif(myrand >= 1 - QGroupBot.NOT_XM_PR):
                    self.res = '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '', self.msg)
        return

    #关键词检测
    def checkKeywords(self):
        if(len(self.res) == 0):
            if(re.search(r'tql|nb|ydl|ddw', self.msg)):
                myrand = random.random()
                if(myrand <= QGroupBot.KW_REPEAT_PR):
                    self.res = self.msg
        return

    #玩梗检测
    def checkMeme(self):
        if(len(self.res) == 0):
            if(re.search(r'(\S[ ]+){3,}', re.sub(ur"[\u4e00-\u9fa5]", 'a', self.msg.decode('gbk')) + ' ')):
                self.res = random.choice(QGroupBot.FIXED_REPLY_DICT['LewdDream'])
            elif(re.search(r'(\S+♂){2,}', self.msg)):
                self.res = random.choice(QGroupBot.FIXED_REPLY_DICT['Philosophy'])
        return

    #跟风复读
    def followRepeat(self):
        if(len(self.res) == 0):
            if(self.mbrArr.count(self.msg) >= 2):
                self.mbrArr = [''] * 10
                self.res = self.msg
            else:
                self.recordMbrMsg()
        return

    #记录
    def recordMbrMsg(self):
        self.mbrArr[self.mbrIndex] = self.msg
        self.mbrIndex = 0 if self.mbrIndex == 9 else self.mbrIndex + 1
        self.lastMsgInvl += 1
        return

    def verify(self):
        if (len(self.res) == 0):
            api_url = QGroupBot.SETTINGS['review_api_url']
            param = {
                'access_token': QGroupBot.SETTINGS['review_access_token'],
                'content': self.msg.decode('gbk').encode('utf-8')
            }
            param = urlencode(param).encode('utf-8')
            labels_type = {
                1: '暴恐违禁',
                2: '文本色情',
                3: '政治敏感',
                4: '恶意推广',
                5: '低俗辱骂',
                6: '低质灌水',
            }
            response = Request(api_url.encode('utf-8'), data=param)
            response = urlopen(response).read().decode('utf-8').encode('gbk')
            for error in json.loads(response, encoding='gbk')['result']['reject']:
                for hit in error['hit']:
                    self.res = self.res + hit + ' '
                self.res = self.res + ' 涉嫌' + labels_type[error['label']] + '\n'
            #     for error in json.loads(response)['result']['review']:
            #         for hit in error['hit']:
            #             ret = ret + hit
            #         ret = ret + ' 涉嫌' + labels_type[error['label']] + '\n'
            if len(self.res) > 0:
                self.res = ('咳咳\n'+self.res[:-1]).encode('gbk')
            logging.info(self.res)
        return

    #随机复读
    def rndRepeat(self):
        if(len(self.res) == 0):
            if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_RE_LEN):
                myrand = random.random()
                if(myrand <= QGroupBot.RND_REPEAT_PR):
                   self.lastMsgInvl = 0
                   self.res = self.msg
        return

    #随机羡慕
    def rndXM(self):
        if(len(self.res) == 0):
            if(len(self.msg) > 2 and not re.search(r'^xm|^羡慕|\?$|？$', self.msg)):
                if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                    myrand = random.random()
                    if(myrand <= QGroupBot.RND_XM_PR):
                        self.lastMsgInvl = 0
                        self.msg = re.sub(r'^我', '', self.msg)
                        self.res = '羡慕' + self.msg
        return

    #避免复读自身/另一个bot
    def checkWord(self):
        if(len(self.res) > 0):
            if(self.res == self.msg and self.res in self.selfArr):
                self.res = ''
                return
            else:
                for wordList in QGroupBot.FIXED_REPLY_DICT.values():
                    if(self.msg in wordList):
                        self.res = ''
                        return
                self.selfArr[self.selfIndex] = self.res
                self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
                sleepTimeRemain = QGroupBot.SLEEP_TIME + self.beginTimeStamp - time.time()
                if(sleepTimeRemain > 0):
                    time.sleep(sleepTimeRemain)
        return