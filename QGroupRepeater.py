# -*- coding:gbk -*-
import random
import time
import re

class QGroupBot:
    
    def __init__(self, fromGroup):
        self.arr = [''] * 10
        self.index = 0
        self.lastmsginvl = 10
        self.lastmsgtime = 0
        self.mylastword = ""
        self.fromGroup = fromGroup
        self.res = ""
        self.msg = ""
    
    def tryRepeat(self, msg):
        self.res = ""
        self.msg = re.sub(r'\[CQ:image,file=.+\]', '', msg)
        self.getWord()
        if(len(self.res)>0):
            if(self.res == self.mylastword):
                self.res = ""
            self.mylastword = self.res
        if(len(self.res)>0):
            time.sleep(random.randint(1,100)/100 + 0.5)
        return self.res
    
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
        if(len(self.res)==0):
            if(self.msg.find("[CQ:at,qq=1414421072]") >= 0):
                self.res = "guna，别烦我"
        return
        
    #xm
    def checkXM(self):
        if(len(self.res)==0):
            if(self.msg[0:2] == "xm" or self.msg[0:4] == "羡慕"):
                myrand = random.random()
                if(myrand <= 0.8):
                    self.res = self.msg
                elif(myrand >= 0.9):
                    self.res = "呸，老子不羡慕"
        return
    
    #keywords
    def checkKeywords(self):
        if(len(self.res)==0):
            if(self.msg[-2:] =="nb" or self.msg[-3:] == "ydl" or self.msg[0:3] == "tql" or self.msg[-3:] == "tql" or self.msg[-3:] == "ddw"):
                myrand = random.random()
                if(myrand <= 1):
                    self.res = self.msg
        return
    
    #跟风复读
    def followRepeat(self):
        if(len(self.res)==0):
            for words in self.arr:
                if(words == self.msg):
                    self.arr = [''] * 10
                    self.res = self.msg
                    break
        if(len(self.res)==0):
            self.recordMsg()
        return
        
    #记录
    def recordMsg(self):
        self.arr[self.index] = self.msg
        self.index += 1 
        if(self.index == 10):
            self.index = 0;
        self.lastmsginvl += 1
        return
        
    #随机复读
    def rndRepeat(self):
        if(len(self.res)==0):
            if(self.lastmsginvl > 5 and len(self.msg) <= 20):
                myrand = random.random()
                if(myrand <= 0.05):
                   self.lastmsginvl = 0
                   self.res = self.msg
        return
        
    #随机羡慕
    def rndXM(self):
        if(len(self.res)==0):
            if(self.msg[-1] != "?" and self.msg[-1] != "？"):
                if(self.lastmsginvl > 5 and len(self.msg) <= 16):
                    myrand = random.random()
                    if(myrand <= 0.05):
                        self.lastmsginvl = 0
                        self.res = "羡慕" + self.msg
        return
    
    
    
    
    
    
    
    
    
    
