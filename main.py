try:
    import ujson
except:
    import json as ujson

import network
import ntptime
import urequests
import utime
from machine import Timer, idle

from Scenes import Scenes

PUBLISH = "publish"  # type: str
CALL = "call"  # type: str
HOST = ""  # type: str
URI = ""  # type:str


def publish(_id, value):
    data = {
        "topic": URI + ".measurement." + _id + ".create",
        "args": [ujson.dumps({
            "sensor": _id,
            "timestamp": utime.localtime()[0:6],
            "value": value
        })]
    }
    post(data, PUBLISH)


def call(_id):
    data = {
        "procedure": URI + ".actuator." + _id,
        "args": []
    }
    post(data, CALL)


def post(data, method):
    r = urequests.post("https://" + HOST + "/" + method, json=data)
    r.close()


class Device:
    def __init__(self, env):
        self.sta = network.WLAN(network.STA_IF)  # type: network
        self.sta.active(True)
        self.scenes = Scenes(publish=publish, call=call)  # type: Scenes
        if env.get('crossbar') and env.get('crossbar').get('host'):
            global URI, HOST
            HOST = env.get('crossbar').get('host', "")  # type: str
            for index, item in enumerate(HOST.split('.')):
                if index > 0:
                    URI = item + '.' + URI
                else:
                    URI = item
            print(URI)
        else:
            raise Exception('Crossbar Host not found!')
        if env.get('wireless') and env.get('wireless').get('ssid') and env.get('wireless').get('password'):
            self.sta.connect(env.get('wireless').get('ssid'), env.get('wireless').get('password'))
            count = 0
            while not self.sta.status() == network.STAT_GOT_IP and count < 5:
                utime.sleep_ms(500)
                count += 1
            try:
                ntptime.settime()
            except:
                pass
        if env.get('scenes'):
            for item in env.get('scenes'):
                self.scenes.add_sensors(item)
        self.timer = Timer(0)
        self.timer.init(mode=Timer.PERIODIC, period=60000, callback=self.read_sensors)

    def read_sensors(self, t=None):
        for scene in self.scenes.sensors:
            for _id, data in scene.values():
                publish(_id, data)


if __name__ == '__main__':
    with open('env.json', 'r') as f:
        device = Device(ujson.loads(f.read()))
    while True:
        idle()
