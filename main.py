try:
    import ujson
except:
    import json as ujson

import network
import ntptime
import urequests
import utime
from machine import Pin, Timer, idle

from Humidity import Humidity, Humidity_Sensor
from Temperature import Temperature, Temperature_Sensor


class Device:
    def __init__(self, env):
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.scenes = []
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
                if item['type'] == 'Humidity':
                    self.scenes.append(
                        Humidity(Pin(item['pin'], Pin.PULL_UP), getattr(Humidity_Sensor, item['pattern']), item['_id']))
                elif item['type'] == 'Temperature':
                    self.scenes.append(
                        Temperature(Pin(item['pin'], Pin.PULL_UP), getattr(Temperature_Sensor, item['pattern']),
                                    item['_id']))

        utime.sleep(2)
        self.read_sensors()
        self.timer.init(mode=Timer.PERIODIC, period=1800000, callback=self.read_sensors)

    def read_sensors(self, t=None):
        for scene in self.scenes:
            self.set_data(scene.get_id(), scene.read())

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
