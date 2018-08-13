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
        self.beginTimeStamp = 0
        self.res = ""
        self.msg = ""
    
    def responseMsg(self, msg):
        self.beginTimeStamp = time.time()
        self.res = ""
        #ȥ����β�հ�
        self.msg = msg.strip().strip("\n")
        #ȥ��CQ��ͼƬ
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', self.msg)
        #ȥ����CQ�����
        self.msg = re.sub(r'/��|/Ц��|/doge|/�ᱼ|/����|/����|/����|/б��Ц|/��Ѫ|/��ϲ|/ɧ��|/С����|/������|/��|/��|/���|/��з|/����|/�ջ�|/����|/��Ц|/������|/��Į|/��|/�ð�|/����|/����|/����|/����|/��|/�ͻ�|/����|/����|/С����|/���|/�Ҳ���|/��|/����|/��ͷ|/��һ��|/��һ��|/��һ��|/קը��|/������', '', self.msg)
        self.getWord()
        self.checkWord()            
        return self.res
    
    #��ȡ�ظ�����
    def getWord(self):
        self.replyAT()
        self.checkXM()
        self.checkKeywords()
        self.checkStink()
        self.followRepeat()
        self.rndRepeat()
        self.rndXM()
        return
    
    #�ظ�����
    def replyAT(self):
        if(len(self.res) == 0):
            if(re.match(r'\[CQ:at,qq=2279711715\]', self.msg)):
                self.res = "guna������"
        return
        
    #��Ľ���
    def checkXM(self):
        if(len(self.res) == 0):
            if(re.match(r'xm|��Ľ', self.msg)):
                myrand = random.random()
                if(myrand <= QGroupBot.XM_PR):
                    self.res = self.msg
                elif(myrand >= 1 - QGroupBot.NOT_XM_PR):
                    self.res = "�ޣ����Ӳ���Ľ"
        return
    
    #�ؼ��ʼ��
    def checkKeywords(self):
        if(len(self.res) == 0):
            if(re.search(r'tql|nb|ydl|ddw', self.msg)):
                myrand = random.random()
                if(myrand <= QGroupBot.KW_REPEAT_PR):
                    self.res = self.msg
        return
        
    #�� �� �� ��
    def checkStink(self):
        if(len(self.res) == 0):
            if(re.search(r'(.\s){3}', self.msg)):
                self.res = "�� ˵ �� �� �� ��"
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
            if(len(self.msg) > 2 and not re.search(r'^xm|^��Ľ|?$|��$', self.msg)):
                if(self.lastMsgInvl > QGroupBot.MIN_MSG_INVL and len(self.msg) <= QGroupBot.MAX_RND_XM_LEN):
                    myrand = random.random()
                    if(myrand <= QGroupBot.RND_XM_PR):
                        self.lastMsgInvl = 0
                        self.msg = re.sub(r'^��', '', self.msg)
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
                sleepTimeRemain = QGroupBot.SLEEP_TIME + self.beginTimeStamp - time.time()
                if(sleepTimeRemain > 0):
                    time.sleep(sleepTimeRemain)
        return
    
    
    
    
    
    
    
    