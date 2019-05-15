class Sensor(object):
    """
        Returns a list of tuples with _id and the function that return the value
    """

    def values(self):
        raise NotImplementedError()

    def get_sensor(self):
        raise NotImplementedError()

    def add_id(self):
        raise NotImplementedError()
