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
    
    #��ȡ�ظ�����
    def getWord(self):
        self.replyAT()
        self.checkXM()
        self.checkKeywords()
        self.followRepeat()
        self.rndRepeat()
        self.rndXM()
        return
    
    #�ظ�����
    def replyAT(self):
        if(len(self.res) == 0):
            if(self.msg.find("[CQ:at,qq=2279711715]") >= 0):
                self.res = "guna������"
        return
        
    #xm
    def checkXM(self):
        if(len(self.res) == 0):
            if(self.msg[0:2] == "xm" or self.msg[0:4] == "��Ľ"):
                myrand = random.random()
                if(myrand <= QGroupBot.XM_PR):
                    self.res = self.msg
                elif(myrand >= 1 - QGroupBot.NOT_XM_PR):
                    self.res = "�ޣ����Ӳ���Ľ"
        return
    
    #�ؼ���
    def checkKeywords(self):
        if(len(self.res) == 0):
            if(self.msg.find("nb") >= 0 or self.msg.find("ydl") >= 0 or self.msg.find("tql") >= 0 or self.msg.find("ddw") >= 0):
                myrand = random.random()
                if(myrand <= QGroupBot.KW_REPEAT_PR):
                    self.res = self.msg
        return
    
    #���縴��
    def followRepeat(self):
        if(len(self.res) == 0):
            if(self.msg in self.mbrArr):
                self.mbrArr = [''] * 10
                self.res = self.msg
            else:
                self.recordMbrMsg()
        return
        
    #��¼
    def recordMbrMsg(self):
        self.mbrArr[self.mbrIndex] = self.msg
        self.mbrIndex = 0 if self.mbrIndex == 9 else self.mbrIndex + 1
        self.lastMsgInvl += 1
        return
        
    #�������
    def rndRepeat(self):
        if(len(self.res) == 0):
            if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_RE_LEN):
                myrand = random.random()
                if(myrand <= QGroupBot.RND_REPEAT_PR):
                   self.lastMsgInvl = 0
                   self.res = self.msg
        return
        
    #�����Ľ
    def rndXM(self):
        if(len(self.res) == 0):
            if(self.msg[-1] != "?" and self.msg[-1] != "��" and self.msg[0:2] != "xm" and self.msg[0:4] != "��Ľ" ):
                if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                    myrand = random.random()
                    if(myrand <= QGroupBot.RND_XM_PR):
                        self.lastMsgInvl = 0
                        if(self.msg[0:2] == "��"):
                            self.msg = self.msg[3:]
                        self.res = "��Ľ" + self.msg
        return
    
    #���⸴������
    def checkWord(self):
        if(len(self.res) > 0):
            if(self.res in self.selfArr):
                self.res = ""
            else:
                self.selfArr[self.selfIndex] = self.res
                self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
                time.sleep(QGroupBot.SLEEP_TIME)
        return
    
    
    
    
    
    
    
    