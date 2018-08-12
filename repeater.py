# -*- coding: utf-8 -*-

GROUPS_TO_REPEAT = ['2842243415', '1675087388']
BLACKLIST = ['682881741', ]

last_message = {}
last_sent = ""

stop_countdown = 0


def onQQMessage(bot, contact, member, content):
    if content == ""\
            or contact.ctype != 'group'\
            or contact.uin not in GROUPS_TO_REPEAT\
            or member.uin in BLACKLIST:
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
    if group_name in last_message.keys() and last_message[group_name][0] == content:
        last_message[group_name][1] += 1
        if last_message[group_name][1] == 2:
            if content != last_sent:
                last_sent = content
                bot.SendTo(contact, content)
    else:
        last_message[group_name] = [content, 1]
