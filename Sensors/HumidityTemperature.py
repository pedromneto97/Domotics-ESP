from machine import Pin
from utime import ticks_ms, ticks_diff

from Sensors.Sensor import Sensor


class HumidityTemperatureSensor:
    DHT11 = 0
    DHT22 = 1
    AM2320 = 1


class HumidityTemperature(Sensor):
    def __init__(self, **kwargs):
        if len(kwargs.get('pins', [])) == 0:
            raise Exception("Pin required")
        if kwargs.get('sensor_type') is None:
            raise Exception('Sensor Type required')
        if kwargs.get('sensor') is None:
            raise Exception('Sensor required')
        if kwargs.get('_id') is None:
            raise Exception('Id required')

        self.pins = kwargs.get('pins')
        self.temperature_id = None
        self.humidity_id = None

        self.add_id(kwargs.get('sensor'), kwargs.get('_id'))

        # Name of HumidityTemperatureSensor atr
        self.sensor_type = kwargs.get('sensor_type')

        self._last_measure = None
        self._last_temperature = None
        self._last_humidity = None

        sensor_value = getattr(HumidityTemperatureSensor, self.sensor_type)

        if sensor_value == 0:
            from dht import DHT11
            self.sensor = DHT11(Pin(self.pins[0], Pin.PULL_UP))
        elif sensor_value == 1:
            from dht import DHT22
            self.sensor = DHT22(Pin(self.pins[0], Pin.PULL_UP))
        else:
            raise Exception('sensor not available')

    def measure(self):
        _now = ticks_ms()
        if self._last_measure is None or ticks_diff(_now, self._last_measure) >= 2:
            self._last_measure = _now
            self.sensor.measure()

    def values(self):
        self.measure()
        humidity = self.sensor.humidity()
        temperature = self.sensor.temperature()
        values = []
        if self._last_humidity is None or humidity - self._last_humidity > 0.5:
            values.append((self.humidity_id, humidity))
        if self._last_temperature is None or temperature - self._last_temperature > 0.5:
            values.append((self.temperature_id, temperature))
        return values

    def get_sensor(self, type, pins):
        return type == self.sensor_type and pins == self.pins

    def add_id(self, type, _id):
        if type == 'TEMPERATURE':
            self.temperature_id = _id
        elif type == 'HUMIDITY':
            self.humidity_id = _id
        else:
            raise Exception('Invalid tyṕe')
