from aiocqhttp import CQHttp, ApiError
import os
import random
import QGroupRepeater
import logging
import asyncio
import time
from util import load_json
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'QQGroupRepeater.log'),
    filemode='w+')

bot = CQHttp(api_root='http://127.0.0.1:5700/')

GroupDict = dict()
SETTINGS = load_json("settings.json")
REPLY = load_json('reply.json')


@bot.on_message('private')
async def handle_private(context):
    await bot.send(context, message=context['message'])
    if context['user_id'] in SETTINGS['ADMIN']:
        for group_id in SETTINGS['REPOST_GROUP']:
            await bot.send({'group_id': group_id}, message=context['message'])


@bot.on_message('group')
async def handle_msg(context):
    groupId = context['group_id']
    if groupId not in SETTINGS['ALLOW_GROUP']:
        return
    global GroupDict
    try:
        if (GroupDict.get(groupId) == None):
            GroupDict[groupId] = QGroupRepeater.Bot(groupId)
        re = GroupDict[groupId].responseMsg(context)
        print(context['message'], re)
        return await bot.send(context, message=re) if (len(re) > 0) else 0
    except Exception as e:
        logging.exception(e)


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    if context['group_id'] not in SETTINGS['ALLOW_GROUP']:
        return
    re = random.choice(REPLY['on_group_increase'])
    await bot.send(context, message=re, auto_escape=True)


@bot.on_request('group', 'friend')
async def handle_group_request(context):
    return {'approve': True}


async def send_early_msg():
    await asyncio.sleep(int(random.random() * 60 * 60) + 900)
    time_format = "%Y-%m-%d %H:%M:%S"
    bj_offset = timezone(timedelta(hours=8))
    bj_datetime = datetime.now(bj_offset)
    re = random.choice(REPLY['on_early'])
    for group_id in SETTINGS['MEMTION_GROUP']:
        await bot.send({'group_id': group_id}, message=re)


async def send_new_day_msg():
    for group_id in SETTINGS['MEMTION_GROUP']:
        re = random.choice(REPLY['on_new_day'])
        await bot.send({'group_id': group_id}, message=re)


def sche():
    scheduler = AsyncIOScheduler()
    # TODO: fit for all environments with different timezone, this is for 0 timezone
    scheduler.add_job(send_early_msg, 'cron', hour="20", minute="0")
    scheduler.add_job(send_new_day_msg, 'cron', hour="16", minute="0")
    scheduler.start()


if __name__ == '__main__':
    sche()
    bot.run(host='127.0.0.1', port=8090)
