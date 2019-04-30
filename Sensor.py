class Sensor(object):
    def read(self):
        raise NotImplementedError()

    def get_id(self):
        return self._id
