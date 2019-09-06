import os
import re
import json


def load_json(file_name):
    file_path = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], file_name)
    try:
        return json.load(open(file_path, 'r', encoding='UTF-8'))
    except:
        print(f"load {file_name} failed")
        return None

def purgeMsg(msg):
    msg = msg.replace('\r', '')
    msg = re.sub(r'\[CQ:image,file=.+\]', '', msg)
    msg = re.sub(r'\[CQ:face,id=\d+\]', '', msg)
    msg = re.sub(r'\[CQ:at,qq=\d+\]', '', msg)
    msg = re.sub(
        r'/舔|/笑哭|/doge|/泪奔|/无奈|/托腮|/卖萌|/斜眼笑|/喷血|/惊喜|/骚扰|/小纠结|/我最美|' + \
        r'/茶|/蛋|/红包|/河蟹|/羊驼|/菊花|/幽灵|/大笑|/不开心|/冷漠|/呃|/好棒|/拜托|/点赞|' + \
        r'/无聊|/托脸|/吃|/送花|/害怕|/花痴|/小样儿|/飙泪|/我不看|/啵啵|/糊脸|/拍头|/扯一扯|' + \
        r'/舔一舔|/蹭一蹭|/拽炸天|/顶呱呱',
        '', msg)
    msg = msg.replace('\n', ' ')
    msg = msg.strip()
    return msg
