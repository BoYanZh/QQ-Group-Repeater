import re
from flask import jsonify, Flask, request
from util import load_json
from queue import Queue
import random
import requests
import time


class MsgManager():
    DELAY_SECONDS = 5
    CONG_COUNT = 3

    def __init__(self):
        self.msg = []
        self.count = 0
        self.congCount = 0
        self.drawing = False
        self.lastCongTime = time.time()
        self.congMsg = ''
        self.danmuDB = {}
        self.queryTime = {}
        self.lastUpdateTime = time.time()

    def cong(self):
        for i in range(10):
            self.msg.append(f"#admin #rainbow " + self.congMsg)
        self.lastCongTime = time.time()
        self.congCount -= 1

    def update(self):
        if time.time() - self.lastUpdateTime < 0.5:
            return
        jsonRes = requests.get('http://127.0.0.1:8090/danmu/coolq').json()
        if jsonRes:
            timeNow = time.time()
            uDB[timeNow] = jsonRes
            for key in self.danmuDB.keys():
                if timeNow - key > 30:
                    self.danmuDB.pop(key)

    def get(self, addr):
        self.update()
        self.msg = []
        timeNow = time.time()
        if self.congCount and timeNow - self.lastCongTime > MsgManager.DELAY_SECONDS:
            self.cong()
        if self.queryTime.get(addr) is None:
            self.queryTime[addr] = 0
        # jsonRes = requests.get('http://127.0.0.1:8090/danmu/coolq').json()
        # if not jsonRes:
        #     return self.msg
        for t, msgs in self.danmuDB:
            if t < self.queryTime[addr]:
                continue
            for data in msgs:
                if data['from'] not in SETTINGS.get('DANMU_GROUP'):
                    continue
                if self.drawing:
                    self.count -= 1
                    if self.count == 0:
                        print('\n\n\n\ndrawed\n\n\n\n')
                        self.congMsg = f"恭喜 {data['sender']['nickname']}({data['sender']['user_id']}) 中奖啦！"
                        self.msg.append("#admin #cong " + self.congMsg)
                        self.congCount = MsgManager.CONG_COUNT
                        self.cong()
                        self.drawing = False
                if data['sender']['user_id'] in SETTINGS.get('DANMU_ADMIN'):
                    data['msg'] = '#admin' + data['msg']
                    if '#start' in data['msg']:
                        self.drawing = True
                        self.count = random.randint(5, 10)
                        print(self.count)
                    else:
                        self.msg.append(data['msg'])
                else:
                    data['msg'] = data['msg'].replace('#admin', '')
                    self.msg.append(data['msg'])
        return self.msg


app = Flask(__name__)
SETTINGS = load_json('settings.json')
danmuDB = []
msgManager = MsgManager()
drawMode = False


@app.route('/danmu/dmpush')
def danmu():
    return jsonify(msgManager.get(request.remote_addr))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)
