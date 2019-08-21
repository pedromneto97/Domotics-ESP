from machine import Pin
from utime import ticks_ms, ticks_diff

from Sensors.Sensor import Sensor

try:
    from typing import List, Callable
except:
    pass


class Presence(Sensor):
    def __init__(self, **kwargs):
        if len(kwargs.get('pins', [])) == 0:
            raise Exception("Pin required")
        if kwargs.get('sensor_type') is None:
            raise Exception('Sensor Type required')
        if kwargs.get('_id') is None:
            raise Exception('Id required')
        if kwargs.get('publish') is None:
            raise Exception('Publish callback required')
        if kwargs.get('call') is None:
            raise Exception('Call callback required')

        self.pins = kwargs.get('pins')  # type: List[int]
        self.input = Pin(self.pins[0], Pin.IN)
        self.input.irq(handler=self.change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

        # Name of HumidityTemperatureSensor atr
        self.sensor_type = kwargs.get('sensor_type')
        self.type = kwargs.get('sensor')
        self.add_id(kwargs.get('_id'))

        self.publish = kwargs.get('publish')  # type: Callable
        self.call = kwargs.get('call')

        self.last_value = 0  # type: int
        self.last_tick = ticks_ms()  # type: int

    def change(self, p):
        value = p.value()  # type: int
        tick = ticks_ms()  # type: int
        if ticks_diff(tick, self.last_tick) > 200 or self.last_value != value:
            self.last_value = value
            self.last_tick = tick
            self.publish(self._id, value)
            self.call(self._id)

    def values(self):
        values = [(self._id, self.input.value())]
        return values

    def get_sensor(self, type, pins):
        return pins == self.pins

    def add_id(self, _id):
        self._id = _id
