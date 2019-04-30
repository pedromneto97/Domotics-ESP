from Sensor import Sensor


class Humidity_Sensor:
    DHT11 = 0
    DHT22 = 1
    AM2320 = 1


class Humidity(Sensor):
    def __init__(self, pin, sensor_type: str, _id):
        self.pin = pin
        self._id = _id
        if sensor_type == 0:
            from dht import DHT11
            self.sensor = DHT11(pin)
        elif sensor_type == 1:
            from dht import DHT22
            self.sensor = DHT22(pin)
        else:
            raise Exception('sensor not available')

    def read(self):
        self.sensor.measure()
        return self.sensor.humidity()
