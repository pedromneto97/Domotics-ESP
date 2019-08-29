from machine import Pin
from utime import ticks_ms, ticks_diff

from Sensors.Sensor import Sensor


class HumidityTemperatureSensor:
    DHT11 = 0
    DHT22 = 1
    AM2320 = 1


class HumidityTemperature(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temperature_id = None
        self.humidity_id = None

        self.add_id(self.sensor, kwargs.get('_id'))

        self._last_measure = None

        sensor_value = getattr(HumidityTemperatureSensor, self.pattern)

        if sensor_value == 0:
            from dht import DHT11
            self.sensor = DHT11(Pin(self.pins[0], Pin.PULL_UP))
        elif sensor_value == 1:
            from dht import DHT22
            self.sensor = DHT22(Pin(self.pins[0], Pin.PULL_UP))
        else:
            raise Exception('sensor not available')
        self._last_temperature = None
        self._last_humidity = None

    def measure(self):
        _now = ticks_ms()
        if self._last_measure is None or ticks_diff(_now, self._last_measure) >= 2000:
            self._last_measure = _now
            self.sensor.measure()

    def values(self):
        self.measure()
        humidity = self.sensor.humidity()
        temperature = self.sensor.temperature()
        values = []
        if self._last_humidity is None or abs(humidity - self._last_humidity) > (self._last_humidity / 100.0):
            self._last_humidity = humidity
            values.append((self.humidity_id, humidity))
        if self._last_temperature is None or abs(temperature - self._last_temperature) > 0.2:
            self._last_temperature = temperature
            values.append((self.temperature_id, temperature))
        return values

    def get_sensor(self, pattern, pins):
        return pattern == self.pattern and pins == self.pins

    def add_id(self, sensor_type, _id):
        if sensor_type == 'TEMPERATURE':
            self.temperature_id = _id
        elif sensor_type == 'HUMIDITY':
            self.humidity_id = _id
        else:
            raise Exception('Invalid tyṕe')
