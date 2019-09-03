from machine import Pin
from utime import ticks_ms, ticks_diff

from Sensors.Sensor import Sensor

try:
    from typing import List, Callable
except:
    pass


class Presence(Sensor):
    def __init__(self, **kwargs):
        super(Presence, self).__init__(**kwargs)
        if kwargs.get('publish') is None:
            raise Exception('Publish callback required')
        if kwargs.get('call') is None:
            raise Exception('Call callback required')
        elif kwargs.get('calls') is None:
            raise Exception('Ids are required')

        self._id = None
        self.add_id(self.sensor, kwargs.get('_id'))
        self.input = Pin(self.pins[0], Pin.IN)  # type: Pin
        self.input.irq(handler=self.change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

        self.type = kwargs.get('sensor')  # type: str

        self.publish = kwargs.get('publish')  # type: Callable
        self.call = kwargs.get('call')  # type: Callable

        self.calls = kwargs.get('calls')  # type: List[str]

        self.last_value = 0  # type: int
        self.last_tick = ticks_ms()  # type: int

    def change(self, p):
        value = p.value()  # type: int
        tick = ticks_ms()  # type: int
        if self.last_value != value and ticks_diff(tick, self.last_tick) > 200:
            print(self._id)
            print(value)
            self.last_value = value
            self.last_tick = tick
            self.publish(self._id, value)
            for id in self.calls:
                self.call(id)

    def values(self):
        values = [(self._id, self.input.value())]
        return values

    def get_sensor(self, sensor_type, pins):
        return pins == self.pins

    def add_id(self, sensor_type, _id):
        print("Id: " + _id)
        self._id = _id
