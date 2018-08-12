# -*- coding: utf-8 -*-
import random
import time
import re

class QGroupBot:
    
    def __init__(self, fromGroup):
        logging.info('OnEvent_GroupMsg: {0}'.format(fromGroup))
        self.arr = [''] * 10
        self.index = 0
        self.lastmsginvl = 10
        self.lastmsgtime = 0
        self.mylastword = ""
        self.fromGroup = fromGroup
    
    def tryRepeat(self, msg):
        res = ""
        #if(time.time() - self.lastmsgtime >= 3):
        #msg = msg.decode("utf-8").encode("gbk")
        res = self.getWord(msg)
        if(res != ""):
            res = res.decode("utf-8").encode("gbk")
            self.lastmsgtime = time.time()
            self.mylastword = res
        return res
        
    def getWord(self, msg):
        #字符处理
        msg = re.sub(r'\[CQ:image,file=.+\]', '', msg)
        mymsg = msg.lower()
        '''if(msg=="list"):
            return repr(self.arr)'''
        #@回复
        if(msg.find("[CQ:at,qq=2279711715]") >= 0):
            return "guna，别烦我"
        #xm/nb
        if(mymsg[0:2] == "xm" or mymsg[0:2] == "羡慕"):
            myrand = random.random()
            if(myrand <= 0.6):
                return msg
            elif(myrand >= 0.9):
                return "呸，老子不羡慕"
        if(mymsg[-2:] =="nb" or mymsg[0:3] == "ydl" \
           or mymsg[0:3] == "tql" or mymsg[-3:] == "tql" \
           or mymsg[-3:] == "ddw"):
            myrand = random.random()
            if(myrand <= 0.6):
                return msg
        #跟风复读
        for words in self.arr:
            if(words == mymsg):
                self.arr = [''] * 10
                return msg
        #随机复读
        if(self.lastmsginvl > 5 and len(mymsg) <= 20):
            myrand = random.random()
            if(myrand <= 0.1):
               self.lastmsginvl = 0
               return msg
        #随机羡慕
        if(mymsg[-1] != "?" and mymsg[-1] != "？"):
            if(self.lastmsginvl > 5 and len(mymsg) <= 16):
                myrand = random.random()
                if(myrand <= 0.2):
                    self.lastmsginvl = 0
                    return "羡慕" + msg
        #记录
        self.arr[self.index] = mymsg
        self.index += 1 
        if(self.index == 10):
            self.index = 0;
        self.lastmsginvl += 1
        return ""
    
    ###.decode("utf-8").encode("gbk")