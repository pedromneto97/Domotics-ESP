from Sensors.HumidityTemperature import HumidityTemperature
from Sensors.Presence import Presence
from Sensors.Sensor import Sensor


class SensorsTypes:
    DHT11 = 0
    DHT22 = 0
    AM2320 = 0
    HCSR501 = 1


class Scenes:
    def __init__(self):
        self.sensors = []  # type: [Sensor]

    def add_sensors(self, **kwargs):
        # Check kwargs
        if kwargs.get('pins') is None or kwargs.get('sensor_type') is None or kwargs.get('_id') is None or kwargs.get(
                'type') is None:
            raise Exception('arg required not found')

        # if already has the sensor
        sensor = self.has_sensors_type(kwargs.get('sensor_type'), kwargs.get('pins'))
        if sensor is not None:
            sensor.add_id(kwargs.get('type'), _id=kwargs.get('_id'))
            return

        # if does not exists, append to list
        if getattr(SensorsTypes, kwargs.get('sensor_type')) == 0:
            self.sensors.append(HumidityTemperature(pins=kwargs.get('pins'), sensor_type=kwargs.get('sensor_type'),
                                                    sensor=kwargs.get('type'), _id=kwargs.get('_id')))
        elif getattr(SensorsTypes, kwargs.get('sensor_type')) == 1:
            self.sensors.append(Presence(pins=kwargs.get('pins'), sensor_type=kwargs.get('sensor_type'),
                                         sensor=kwargs.get('type'), _id=kwargs.get('_id'), call=kwargs.get('call'),
                                         publish=kwargs.get('publish')))

    def has_sensors_type(self, sensor_type, pins):
        for item in self.sensors:
            if item.get_sensor(sensor_type, pins):
                return item
        return None
