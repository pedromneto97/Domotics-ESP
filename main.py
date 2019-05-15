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


class Device:
    def __init__(self, env):
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.scenes = Scenes()
        self.timer = Timer(0)
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
        utime.sleep_ms(200)
        if env.get('scenes'):
            for item in env.get('scenes'):
                self.scenes.add_sensors(type=item['type'], sensor_type=item['pattern'], _id=item['_id'])

        utime.sleep(2)
        self.read_sensors()
        self.timer.init(mode=Timer.PERIODIC, period=1800000, callback=self.read_sensors)

    def read_sensors(self, t=None):
        for scene in self.scenes.sensors:
            for _id, data in scene.values():
                self.set_data(_id, data)
        idle()

    @staticmethod
    def set_data(_id, value):
        data = {
            "topic": "com.herokuapp.crossbar-pedro.measurement." + _id + ".create",
            "args": [ujson.dumps({
                "sensor": _id,
                "timestamp": utime.localtime()[0:6],
                "value": value
            })]
        }
        r = urequests.post("https://crossbar-pedro.herokuapp.com/publish", json=data)
        r.close()


with open('.env', 'r') as f:
    device = Device(ujson.loads(f.read()))
idle()
