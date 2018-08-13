# -*- coding:gbk -*-
import random
import time
import re

class QGroupBot:
    
    XM_PR = 0.8
    NOT_XM_PR = 0.1
    RND_REPEAT_PR = 0.05
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
        self.myLastWord = ""
        self.res = ""
        self.msg = ""
    
    def responseMsg(self, msg):
        self.res = ""
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', msg)
        self.getWord()
        self.checkWord()            
        return self.res
    
    #获取回复内容
    def getWord(self):
        self.replyAT()
        self.checkXM()
        self.checkKeywords()
        self.followRepeat()
        self.rndRepeat()
        self.rndXM()
        return
    
    #回复艾特
    def replyAT(self):
        if(len(self.res) == 0):
            if(self.msg.find("[CQ:at,qq=2279711715]") >= 0):
                self.res = "guna，别烦我"
        return
        
    #xm
    def checkXM(self):
        if(len(self.res) == 0):
            if(self.msg[0:2] == "xm" or self.msg[0:4] == "羡慕"):
                myrand = random.random()
                if(myrand <= QGroupBot.XM_PR):
                    self.res = self.msg
                elif(myrand >= 1 - QGroupBot.NOT_XM_PR):
                    self.res = "呸，老子不羡慕"
        return
    
    #关键词
    def checkKeywords(self):
        if(len(self.res) == 0):
            if(self.msg.find("nb") >= 0 or self.msg.find("ydl") >= 0 or self.msg.find("tql") >= 0 or self.msg.find("ddw") >= 0):
                myrand = random.random()
                if(myrand <= QGroupBot.KW_REPEAT_PR):
                    self.res = self.msg
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
            if(self.msg[-1] != "?" and self.msg[-1] != "？" and self.msg[0:2] != "xm" and self.msg[0:4] != "羡慕" ):
                if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                    myrand = random.random()
                    if(myrand <= QGroupBot.RND_XM_PR):
                        self.lastMsgInvl = 0
                        if(self.msg[0:2] == "我"):
                            self.msg = self.msg[3:]
                        self.res = "羡慕" + self.msg
        return
    
    #避免复读自身
    def checkWord(self):
        if(len(self.res) > 0):
            if(self.res in self.selfArr):
                self.res = ""
            else:
                self.selfArr[self.selfIndex] = self.res
                self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
                time.sleep(QGroupBot.SLEEP_TIME)
        return
    
    
    
    
    
    
    
    