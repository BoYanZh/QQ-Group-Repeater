# -*- coding: utf-8 -*-

import requests
import string
import time
import hashlib
import json
import random


# Translator
def requests_for_dst(word):
    api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    my_appid = 20180815000194642
    cyber = 'KVJEzePbERXN23tH69OX'
    salt = str(time.time())[:10]
    final_sign = str(my_appid)+word+salt+cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    paramas = {
        'q':word,
        'from':'zh',
        'to':'en',
        'appid':'%s'%my_appid,
        'salt':'%s'%salt,
        'sign':'%s'%final_sign
        }
    response = requests.get(api_url, params=paramas).content
    json_reads = json.loads(response, encoding='utf-8')
    return json_reads['trans_result'][0]['dst']


# Verify
def verify(word):
    ret = ''
    api_url = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam'
    paramas = {
        'access_token': '24.0399aa268a5c974b3e7e499a62e0447b.2592000.1536916173.282335-11681411',
        'content': word,
    }
    labels_type = {
        1:'暴恐违禁',
        2:'文本色情',
        3:'政治敏感',
        4:'恶意推广',
        5:'低俗辱骂',
        6:'低质灌水',
    }
    response = requests.post(api_url, params=paramas).content
    for error in json.loads(response)['result']['reject']:
        for hit in error['hit']:
            ret = ret + hit
        ret = ret + ' 涉嫌' + labels_type[error['label']] + '\n'
    for error in json.loads(response)['result']['review']:
        for hit in error['hit']:
            ret = ret + hit
        ret = ret + ' 涉嫌' + labels_type[error['label']] + '\n'
    return ret

# Repeater
GROUPS_TO_REPEAT = ['密西根学院2018学生群', '复读万岁']

last_message = {}
last_sent = ""

stop_countdown = 0


def onQQMessage(bot, contact, member, content):
    if content == ""\
            or contact.ctype != 'group'\
            or contact.name not in GROUPS_TO_REPEAT:
        return

    # Handle stop command
    global stop_countdown
    if content == "stop":
        bot.SendTo(contact, '停了停了')
        stop_countdown = 15
    if stop_countdown > 0:
        stop_countdown -= 1
        return

    global last_sent, last_message
    # Repeat
    group_name = str(contact)
    if bot.isMe(contact, member):
        last_message[group_name] = [content, 4]
    elif group_name in last_message.keys() and last_message[group_name][0] == content:
        last_message[group_name][1] += 1
        if last_message[group_name][1] == 2:
            if content != last_sent:
                last_sent = content
                bot.SendTo(contact, content)
    else:
        last_message[group_name] = [content, 1]
        verify_result = verify(content)
        if verify_result:
            bot.SendTo(contact, '咳咳\n' + verify_result[:-1])
