try:
    import ujson
except:
    import json as ujson

import network
import ntptime
import urequests
import utime
from machine import lightsleep, reset

from Scenes import Scenes


class Device:
    def __init__(self, env):
        self.sta = network.WLAN(network.STA_IF)  # type: network
        self.sta.active(True)
        self.scenes = Scenes()  # type: Scenes
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
                self.scenes.add_sensors(type=item['type'], sensor_type=item['pattern'], _id=item['_id'],
                                        pins=item['pins'])

    def read_sensors(self, t=None):
        for scene in self.scenes.sensors:
            for _id, data in scene.values():
                self.set_data(_id, data)

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


if __name__ == '__main__':
    with open('.env', 'r') as f:
        device = Device(ujson.loads(f.read()))
    while device.sta.isconnected():
        lightsleep(60000)
        device.read_sensors()
    reset()
