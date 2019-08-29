try:
    from typing import List, Tuple
except:
    pass


class Sensor(object):

    def __init__(self, **kwargs):
        if len(kwargs.get('pins', [])) == 0:
            raise Exception("Pin required")
        if kwargs.get('pattern') is None:
            raise Exception('Pattern required')
        if kwargs.get('sensor') is None:
            raise Exception('Sensor required')
        if kwargs.get('_id') is None:
            raise Exception('Id required')

        self.pins = kwargs.get('pins')  # type: List[int]
        self.pattern = kwargs.get('pattern')
        self.sensor = kwargs.get('sensor')

    def values(self):
        """
        :rtype: List[Tuple[str, int]]
        :returns List of ids an values
        """
        raise NotImplementedError()

    def get_sensor(self, pattern, pins):
        """
        Get if it's the same sensor
        :param str pattern: pattern of sensor
        :param List[int] pins: list of pins
        :rtype: bool
        """
        raise NotImplementedError()

    def add_id(self, sensor_type, _id):
        """
        Add id to the sensor
        :param str sensor_type: type of sensor
        :param str _id: string of the id
        """
        raise NotImplementedError()
