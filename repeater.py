# -*- coding: utf-8 -*-

# 插件加载方法：
# 1. install & run qqbot
#    pip install qqbot
#    qqbot
# 2. 将本文件保存至 ~/.qqbot-tmp/plugins 目录 （或 c:\user\xxx\.qqbot-tmp\plugins ）
# 3. 在命令行窗口输入：
#    qq plug repeater

last_message = {}


def onQQMessage(bot, contact, member, content):
    name = str(contact)
    if name in last_message.keys() and last_message[name][0] == content:
        last_message[name][1] += 1
        if last_message[name][1] == 2:
            bot.SendTo(contact, content)
    else:
        last_message[name] = [content, 1]

