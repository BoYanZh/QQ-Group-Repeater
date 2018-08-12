# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen, quote
import json
import time
import random

API_KEY = ['1d72111e084c4ba1b6216232c7a603bb', ]
api_index = 0


def result(query_str, username):
    global api_index
    raw_tuling_raw_tuling_url = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY[api_index]
    tuling_url = "%s%s&userid=%d" % (raw_tuling_raw_tuling_url, quote(query_str), abs(hash(username)))
    response = json.loads(urlopen(Request(url=tuling_url)).read())
    if response['code'] == 40004:
        print('change to api', api_index)
        api_index += 1
        return result(query_str, username)
    length = len(response.keys())
    content = response['text']
    if length == 3:
        return content+response['url']
    elif length == 2:
        return content


def onQQMessage(bot, contact, member, content):
    if content == '':
        return
    if contact.ctype == 'buddy' and contact.uin != '2171759360':
        bot.SendTo(contact, result(content, contact))
        return

    if contact.ctype != 'buddy' and member.uin == '2171759360':
        return
    if random.random() < 0.2:
        time.sleep(1)
        bot.SendTo(contact, result(content, contact))
    return
