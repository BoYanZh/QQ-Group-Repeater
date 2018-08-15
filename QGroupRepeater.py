# -*- coding:gbk -*-
import random
import time
import re

class QGroupBot:

    XM_PR = 0.8
    NOT_XM_PR = 0.1
    RND_REPEAT_PR = 0.03
    RND_XM_PR = 0.05
    KW_REPEAT_PR = 1
    MIN_MSG_INVL = 5
    MAX_RND_RE_LEN = 20
    MAX_RND_XM_LEN = 16
    SLEEP_TIME = 0.5

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

    def responseMsg(self, msg):
        self.beginTimeStamp = time.time()
        self.res = ''
        self.isRepeat = True
        #去除首尾空白
        self.msg = msg.strip().strip('\n')
        #去除CQ码图片
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', self.msg)
        #去除非CQ码表情
        self.msg = re.sub(r'/舔|/笑哭|/doge|/泪奔|/无奈|/托腮|/卖萌|/斜眼笑|/喷血|/惊喜|/骚扰|/小纠结|/我最美|/茶|/蛋|/红包|/河蟹|/羊驼|/菊花|/幽灵|/大笑|/不开心|/冷漠|/呃|/好棒|/拜托|/点赞|/无聊|/托脸|/吃|/送花|/害怕|/花痴|/小样儿|/飙泪|/我不看|/啵啵|/糊脸|/拍头|/扯一扯|/舔一舔|/蹭一蹭|/拽炸天|/顶呱呱', '', self.msg)
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
        self.rndRepeat()
        self.rndXM()
        return

    #回复艾特
    def replyAT(self):
        if(len(self.res) == 0):
            if(re.search(r'\[CQ:at,qq=2279711715\]', self.msg)):
                self.res = 'guna，别烦我'
        return

    #羡慕检测
    def checkXM(self):
        if(len(self.res) == 0):
            if(re.search(r'^xm|羡慕', self.msg)):
                myrand = random.random()
                if(myrand <= QGroupBot.XM_PR):
                    self.res = self.msg
                elif(myrand >= 1 - QGroupBot.NOT_XM_PR):
                    self.res = '呸，老子才不羡慕' + re.sub(r'^xm|羡慕', '', self.msg)
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
                self.res = '你 说 话 带 空 格'
            elif(re.search(r'(\S+♂){2,}', self.msg)):
                self.res = random.choice ( ['BOY♂NEXT♂DOOR', 'DEEP♂DARK♂FANTASY', 'ASS♂WE♂CAN', 'Do you like WHAT♂YOU♂SEE', 'SLAVES GET YOUR ASS♂ BACK HERE♂', 'FA♂Q'] )
        return

    #跟风复读
    def followRepeat(self):
        if(len(self.res) == 0):
            if(self.msg in self.mbrArr):
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
            if(len(self.msg) > 2 and not re.search(r'^xm|^羡慕|?$|？$', self.msg)):
                if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                    myrand = random.random()
                    if(myrand <= QGroupBot.RND_XM_PR):
                        self.lastMsgInvl = 0
                        self.msg = re.sub(r'^我', '', self.msg)
                        self.res = '羡慕' + self.msg
        return

    #避免复读自身
    def checkWord(self):
        if(len(self.res) > 0):
            if(self.res == self.msg and self.res in self.selfArr):
                self.res = ''
            else:
                self.selfArr[self.selfIndex] = self.res
                self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
                sleepTimeRemain = QGroupBot.SLEEP_TIME + self.beginTimeStamp - time.time()
                if(sleepTimeRemain > 0):
                    time.sleep(sleepTimeRemain)
        return