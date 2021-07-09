from Bot import Bot
import datetime
import requests
import aiohttp
import random
import json
import six
import os
import re


async def aioGet(url):
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as response:
                if response.status != 200:
                    return ""
                return await response.text()
    except aiohttp.ClientError:
        return ""


def Repeater():
    bot = Bot()

    def getReply(key):
        re = Bot.REPLY.get(key)
        return random.choice(re) if re else ''

    # recursively solve 24 points
    def solve24(num):
        def cleanBracketsFor24(equ):
            equ = list(equ)
            brackets, re = [], []
            for i in range(len(equ)):
                if equ[i] == '(':
                    re.append(i)
                if equ[i] == ')':
                    brackets.append([re.pop(), i])
            for pair in brackets:
                tmpEqu = equ.copy()
                tmpEqu[pair[0]] = ''
                tmpEqu[pair[1]] = ''
                if eval(''.join(tmpEqu)) == 24:
                    equ = tmpEqu
            return ''.join(equ)

        if len(num) == 1:
            try:
                if abs(eval(num[0]) - 24) < 0.00001:
                    re = cleanBracketsFor24(num[0][1:-1])
                    return f'{re} = 24'
            except ZeroDivisionError:
                return None
        for k in '+-*/':
            for i in range(0, len(num)):
                for j in range(0, len(num)):
                    if (i != j):
                        tmp = solve24(num[0:min(i, j)] +
                                      num[min(i, j) + 1:max(i, j)] +
                                      num[max(i, j) + 1:len(num)] +
                                      [f'({num[i]} {k} {num[j]})'])
                        if tmp: return tmp

    @bot.onCommand(r'算\s*((\d{1,5}\s+){3}\d{1,5}\s*)$')
    async def reply24(self):
        tmp_reg = re.search(r'算\s*((\d{1,5}\s+){3}\d{1,5}\s*)$', self.msg)
        res = solve24(tmp_reg.group(1).split())
        return res if res else getReply("24_failed")

    @bot.onCommand(r'扔(.*)')
    async def replyThrow(self):
        tmp_reg = re.search(r'扔(.*)', self.msg)
        keyword = tmp_reg.group(1)
        res = ''
        if keyword in ['骰子', '色子']:
            res = str(random.randint(1, 6))
        elif keyword in ['硬币']:
            coin_re = ['正', '反']
            res = coin_re[random.randint(0, 1)]
        elif '复读' in keyword or 'bot' in keyword:
            res = self.getReply('throw_bot')
            if not res:
                res = f'#扔[CQ:at,qq={self.context["user_id"]}]'
        elif not keyword:
            res = self.getReply('throw_nothing')
        else:
            tmp_re = Bot.TRASHES.get(keyword)
            if tmp_re is not None:
                res = f'{keyword}：{tmp_re}\n'
            tmp_dict = dict()
            for key, value in Bot.NEW_TRASHES.items():
                if keyword.lower() in key.lower():
                    tmp_dict[key] = value
            for key, value in sorted(tmp_dict.items(),
                                     key=lambda d: len(d[0])):
                res = f'{res}{key}：{value}\n'
        res = res.strip('\n')
        return res if res else self.getReply('throw_failed')

    @bot.onCommand(r'(([A-Za-z]{2}|)\d{3})是什么')
    async def replyCourseInfo(self):
        tmp_reg = re.search(r'(([A-Za-z]{2}|)\d{3})是什么', self.msg)
        keyword = tmp_reg.group(1)
        resDict = {}
        for item in Bot.COURSES:
            courseCode = item['courseCode']
            if keyword in courseCode:
                if resDict.get(courseCode) is None:
                    resDict[courseCode] = item.copy()
                    resDict[courseCode]['termName'] = []
                    resDict[courseCode]['teams'] = []
                resDict[courseCode]['termName'].append(item['termName'])
                resDict[courseCode]['teams'].extend(item['teams'])
        res = ''
        for item in resDict.values():
            res += f"课程代码:{item['courseCode']}\n"
            res += f"课程名称:{item['courseName']} {item['courseNameEn']}\n"
            res += f"学分:{item['credit']}\n"
            res += f"开设时间:{', '.join(set(item['termName']))}\n"
            res += f"教师:{', '.join(set(item['teams']))}\n\n"
        res = res.strip()
        return res if res else self.getReply("course_failed")

    @bot.onCommand(r'查([\s\S]{2,})|([\s\S]{2,})是谁')
    async def replyContacts(self):
        tmp_reg = re.search(r'查([\s\S]{2,})|([\s\S]{2,})是谁', self.msg.lstrip('#'))
        keyword = tmp_reg.group(1)
        if not keyword:
            keyword = tmp_reg.group(2)
        keyword = keyword.lower()
        res = ""
        for item in Bot.CONTACTS:
            if keyword in item['name'].lower() or keyword in ''.join(
                [word[0] for word in item['name'].lower().split() if word]):
                res += f"姓名：{item['name']}\n职称：{item['title']}\n办公室：{item['office']}\n电话：{item['tel']}\n邮箱：{item['email']}\n介绍:{item['selfIntrUrl']}\n照片：[CQ:image,file={item['imageUrl']}]\n\n"
        return res.strip() if res else self.getReply("contacts_failed")

    @bot.onCommand(r'([\s\S]{2,})教什么')
    async def replyTeaching(self):
        tmp_reg = re.search(r'([\s\S]{2,})教什么', self.msg.lstrip('#'))
        keyword = tmp_reg.group(1)
        keyword = keyword.lower()
        res = ""
        reDict = dict()
        for item in Bot.COURSES:
            if keyword in [name.lower() for name in item['teams']]:
                if reDict.get(item['courseCode']) is None: reDict[item['courseCode']] = []
                reDict[item['courseCode']].append(item['termName'])
        for key, value in reDict.items():
            res += f"{key} ({', '.join(value)})\n"
        return res.strip() if res else self.getReply("teaching_failed")

    @bot.onCommand(r'第几周')
    async def replyWeek(self):
        d1 = datetime.now()
        d2 = datetime(2020, 5, 11)
        return f"今天 {d1.strftime('%m / %d')} 第 {(d1 - d2).days // 7 + 1} 周"

    @bot.onCommand(r'猫图|猫猫')
    async def replyKitty(self):
        url = "https://api.thecatapi.com/v1/images/search"
        tmpJson = json.loads(await aioGet(url))
        imgUrl = tmpJson[0]["url"]
        return f"[CQ:image,file={imgUrl}]"

    @bot.onCommand(r'狗图|狗狗')
    async def replyKitty(self):
        url = "https://dog.ceo/api/breeds/image/random"
        tmpJson = json.loads(await aioGet(url))
        imgUrl = tmpJson["message"]
        return f"[CQ:image,file={imgUrl}]"

    @bot.onCommand(r'狐狸图|大白猫|fubuki|小狐狸')
    async def replyFubuki(self):
        path = random.choice(self.fbkImgs)
        imgPath = six.moves.urllib_parse.urljoin(
            "file://",
            six.moves.urllib.request.pathname2url(os.path.abspath(path)))
        return f"[CQ:image,file={imgPath}]"

    @bot.onCommand(r'深度抽象\s*(.+)')
    async def replyDeepAbstract(self):
        tmp_reg = re.search(r'深度抽象\s*(.+)', self.msg)
        return self.eh.transform(tmp_reg.group(1), isDeepMode=True)

    @bot.onCommand(r'抽象\s*(.+)')
    async def replyDeepAbstract(self):
        tmp_reg = re.search(r'抽象\s*(.+)', self.msg)
        return self.eh.transform(tmp_reg.group(1))

    @bot.on(r'^xm|^羡慕')
    async def checkXM(self):
        myrand = random.random()
        if myrand <= Bot.SETTINGS['XM_PR']:
            if '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '',
                                   self.msg) not in self.selfArr:
                return self.msg
        elif myrand >= 1 - Bot.SETTINGS['NOT_XM_PR']:  # 避免循环羡慕
            if self.msg not in self.selfArr and \
                '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '', self.msg) \
                not in self.selfArr:
                return '呸，老子才不羡慕' + re.sub(r'^xm|^羡慕', '', self.msg)

    @bot.on(r"问：([\s\S]+)\s+答：([\s\S]+)")
    async def study(self):
        reg = re.search("问：([\s\S]+)\s+答：([\s\S]+)", self.msg)
        if not reg or len(reg.groups()) != 2:
            return
        ask = reg.groups()[0]
        ans = reg.groups()[1]
        if len(ask) <= 2:
            return self.getReply("question_too_short")
        if len(ans) >= 500:
            return self.getReply("answer_too_long")
        if Bot.STUDIED_REPLY.get(ask) is None:
            Bot.STUDIED_REPLY[ask] = {
                "answers": list(),
                "adders": list(),
                "from": list()
            }
        for i, answer in enumerate(Bot.STUDIED_REPLY[ask]["answers"]):
            if ans == answer and Bot.STUDIED_REPLY[ask]["from"][
                    i] == self.context['group_id']:
                return self.getReply("study_failed")
        Bot.STUDIED_REPLY[ask]["answers"].append(ans)
        Bot.STUDIED_REPLY[ask]["adders"].append(self.context['user_id'])
        Bot.STUDIED_REPLY[ask]["from"].append(self.context['group_id'])
        with open("data/study.json", 'w', encoding='UTF-8') as f:
            json.dump(Bot.STUDIED_REPLY, f, ensure_ascii=False, indent=4)
        return self.getReply("study_successful")

    # check keywords
    @bot.on(r'tql|nb|ydl|ddw')
    async def checkKeywords(self):
        if random.random() <= Bot.SETTINGS['KW_REPEAT_PR']:
            return self.msg

    @bot.onCommand(r'色图|涩图')
    async def getSetu(self):
        try:
            if self.fromGroup not in Bot.SETTINGS['ADMIN_GROUP'] and \
                self.context['user_id'] not in Bot.SETTINGS['ADMIN']:
                return
            res = ""
            if re.search(r'他的|她的|它的', self.msg):
                url = "https://yande.re/post.json?limit=1&" + \
                    f"tags=uncensored&page={random.randint(1, 1000)}"
                tmpJson = json.loads(await aioGet(url))
                res = tmpJson[0]['file_url']
            elif re.search(r'色图', self.msg):
                tag = random.choice(
                    ['breasts', 'stockings', 'thighhighs', 'cleavage'])
                url = "https://konachan.net/post.json?" + \
                    f"tags={tag}&page={random.randint(1, 100)}"
                tmpJson = json.loads(await aioGet(url))
                urls = [
                    item['file_url'] for item in tmpJson
                    if item['rating'] == 's'
                ]
                res = random.choice(urls)
            elif re.search(r'涩图', self.msg):
                tag = random.choice(['uncensored'])
                url = "https://konachan.net/post.json?" + \
                    f"tags={tag}&page={random.randint(1, 100)}"
                tmpJson = json.loads(await aioGet(url))
                urls = [
                    item['file_url'] for item in tmpJson
                    if item['rating'] != 's'
                ]
                res = random.choice(urls)
            return f"[CQ:image,file={res}]"
        except:
            return getReply("get_image_failed")

    # reply call
    @bot.on()
    async def replyAT(self):
        if (re.search(r'\[CQ:at,qq={}\]'.format(self.context['self_id']),
                      self.msg)):
            return random.choice(Bot.FIXED_REPLY_DICT['AT'])

    # random repeat
    @bot.on()
    async def rndRepeat(self):
        if self.lastMsgInvl > Bot.SETTINGS['MIN_MSG_INVL'] and len(
                self.msg) <= Bot.SETTINGS['MAX_RND_RE_LEN']:
            myrand = random.random()
            if (myrand <= Bot.SETTINGS['RND_REPEAT_PR']):
                self.lastMsgInvl = 0
                return self.msg

    # random XM
    @bot.on()
    async def rndXM(self):
        if len(self.msg) > 2 and not re.search(r'^xm|^羡慕|\?$|？$', self.msg):
            if (self.lastMsgInvl > Bot.SETTINGS['MIN_MSG_INVL']
                    and len(self.msg) <= Bot.SETTINGS['MAX_RND_XM_LEN']):
                myrand = random.random()
                if (myrand <= Bot.SETTINGS['RND_XM_PR']):
                    self.lastMsgInvl = 0
                    self.msg = re.sub(r'^我的|^我', '', self.msg)
                    return '羡慕' + self.msg

    # check meme & regex replys
    @bot.on()
    async def checkMeme(self):
        for regex, words in Bot.REG_REPLY_DICT.items():
            if re.search(regex, self.msg):
                return random.choice(words)

    @bot.on()
    async def replyStudy(self):
        msg = re.sub(r'\[CQ:image,file=.+\]', '', self.msg)
        for key, value in Bot.STUDIED_REPLY.items():
            if key in msg:
                reList = []
                for i, answer in enumerate(value['answers']):
                    if value["from"][i] in [self.context['group_id']
                                            ] + Bot.SETTINGS['ADMIN_GROUP']:
                        reList.append(answer)
                return random.choice(reList)

    # followd repeat
    @bot.on()
    async def followRepeat(self):
        tmpMsg = self.msg
        if '[CQ:image' in self.msg and 'url' in self.msg and 'file' in self.msg:
            tmpMsg = ','.join(self.msg.split(',')[:2]) + ']'
        if self.mbrArr.count(tmpMsg) >= 2:
            self.mbrArr = [''] * 10
            return self.msg

    return bot


async def test():
    repeater = Repeater()
    re = await repeater.responseMsg({
        'message': "#manuel教什么",
        'self_id': 123456,
        'user_id': 1623464502,
        'group_id': 925787157
    })
    print(re)


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [test(), test()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()