from Sensors.HumidityTemperature import HumidityTemperature
from Sensors.Presence import Presence
from Sensors.Sensor import Sensor

try:
    from typing import List
except:
    pass


class SensorsTypes:
    DHT11 = 0
    DHT22 = 0
    AM2320 = 0
    HCSR501 = 1


class Scenes:
    def __init__(self, **kwargs):
        if kwargs.get("publish") is None:
            raise Exception("Publish callback required")
        if kwargs.get("call") is None:
            raise Exception("Call callback required")
        self.sensors = []  # type: [Sensor]
        self.publish = kwargs.get("publish")
        self.call = kwargs.get("call")

    def add_sensors(self, item):
        # Check item
        if item.get('pins') is None or item.get('pattern') is None or item.get('_id') is None or item.get(
                'type') is None:
            raise Exception('arg required not found')

        # if already has the sensor
        sensor = self.has_sensors_type(item.get('pattern'), item.get('pins'))  # type: Sensor
        if sensor is not None:
            sensor.add_id(item.get('type'), _id=item.get('_id'))
            return

        # if does not exists, append to list
        if getattr(SensorsTypes, item.get('pattern')) == 0:
            self.sensors.append(HumidityTemperature(pins=item.get('pins'), pattern=item.get('pattern'),
                                                    sensor=item.get('type'), _id=item.get('_id')))
        elif getattr(SensorsTypes, item.get('pattern')) == 1:
            self.sensors.append(Presence(pins=item.get('pins'), pattern=item.get('pattern'),
                                         sensor=item.get('type'), _id=item.get('_id'), call=self.call,
                                         publish=self.publish, calls=item.get('call')))

    def has_sensors_type(self, pattern, pins):
        """
        :param str pattern: Pattern of sensor
        :param List[int] pins: List of pins
        :rtype Sensor
        """
        for item in self.sensors:
            if item.get_sensor(pattern, pins):
                return item
        return None
