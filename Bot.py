import random
from datetime import datetime, timezone, timedelta
import re
import glob
from util import load_json


class Bot:
    # settings
    SETTINGS = load_json('settings.json')
    REPLY = load_json('data/reply.json')
    TRASHES = load_json('data/trash.json')
    NEW_TRASHES = load_json('data/new_trash.json')
    STUDIED_REPLY = load_json("data/study.json")
    COURSES = load_json("data/course.json")
    CONTACTS = load_json("data/contacts.json")
    FIXED_REPLY_DICT = REPLY['FIXED_REPLY_DICT']
    REG_REPLY_DICT = REPLY['REG_REPLY_DICT']

    def __init__(self):
        self.running = True
        self.mbrArr = [''] * 10
        self.mbrIndex = 0
        self.selfArr = [''] * 10
        self.selfIndex = 0
        self.lastMsgInvl = 10
        self.lastMsgTime = 0
        self.myLastWord = ''
        self.fromGroup = 0
        self.beginTimeStamp = 0
        self.fbkImgs = list(glob.glob("./data/fubuki/*"))
        self.res = ''
        self.msg = ''
        self.context = {}
        self.msgID = 0
        self.replyTasks = []
        self.currentReplyTask = ""

    def getReply(self, key):
        re = Bot.REPLY.get(key)
        return random.choice(re) if re else ''

    def on(self, regex=[], priority=-1):
        def decorator(func):
            self.replyTasks.append((func, regex, priority))
            self.replyTasks.sort(key=lambda item: item[2])

        return decorator

    def onCommand(self, regex=[], priority=-1):
        if isinstance(regex, str):
            return self.on(['^#', regex], priority)
        return self.on(['^#', *regex], priority)

    async def responseMsg(self, context):
        self.context = context
        # self.beginTimeStamp = time.time()
        self.res = ''
        # self.fromGroup = context['group_id']
        # purge msg
        self.msg = context['message']
        self.msg = self.msg.replace('\r', '')
        self.msg = self.msg.strip().strip('\n')
        if not self.msg:
            return ''
        self.currentReplyTask = ""
        await self.recordMbrMsg()
        await self.getWord()
        await self.checkWord()
        if self.res:
            self.msgID += 1
        return self.res

    # get reply content
    async def getWord(self):
        self.switch()
        if self.res or not self.running:
            return
        for func, regexs, priority in self.replyTasks:
            if isinstance(regexs, str):
                regexs = [regexs]
            for regex in regexs:
                if not re.search(regex, self.msg):
                    break
            else:
                tmpRe = await func(self)
                if tmpRe:
                    self.currentReplyTask = func.__name__
                    self.res = tmpRe
                    return

    # switch on / off of the bot
    def switch(self):
        if len(self.msg) > 5:
            return
        user_id = self.context['user_id']
        if (re.search(r'关|停|锤|砸|闭嘴', self.msg) and re.search(r'复读机', self.msg)) \
                and not re.search(r'已经|不|开', self.msg):
            if self.running:
                t = datetime.now(timezone(timedelta(hours=8)))
                if user_id % (t.month * 100 + t.day) % 100 < Bot.SETTINGS['CLOSE_PR'] * 100 or \
                   user_id in Bot.SETTINGS['ADMIN'] or \
                   user_id in Bot.SETTINGS['ALLOWED_LIST'] and \
                   user_id not in Bot.SETTINGS['DISALLOWED_LIST']:
                    self.running = False
                    self.res = self.getReply('switch_off_successful')
                else:
                    self.res = self.getReply('switch_off_failed')
        elif (re.search(r'开|启动|修', self.msg) and re.search(r'复读机', self.msg))\
                and not re.search(r'已经|不要', self.msg):
            if not self.running:
                myrand = random.random()
                if myrand < Bot.SETTINGS['OPEN_FAILED_PR']:
                    self.res = self.getReply('switch_on_failed')
                else:
                    self.running = True
                    self.res = self.getReply('switch_on_successful')
            else:
                self.res = self.getReply('switch_on_already')

    # avoid repaeting itself / another bot
    async def checkWord(self):
        if self.res == self.msg and self.res in self.selfArr:
            self.res = ''
        else:
            self.selfArr[self.selfIndex] = self.res
            self.selfIndex = 0 if self.selfIndex == 9 else self.selfIndex + 1
            if '[CQ:image' in self.res and 'url' in self.res and 'file' in self.res:
                self.res = ','.join(self.res.split(',')[::2]).replace(
                    'url=', 'file=')

    # record previous messages
    async def recordMbrMsg(self):
        if '[CQ:image' in self.msg and 'url' in self.msg and 'file' in self.msg:
            self.mbrArr[self.mbrIndex] = ','.join(
                self.msg.split(',')[:2]) + ']'
        else:
            self.mbrArr[self.mbrIndex] = self.msg
        self.mbrIndex = 0 if self.mbrIndex == 9 else self.mbrIndex + 1
        self.lastMsgInvl += 1
