from . import Driver


class Sensor(Driver):
    __name__ = "Sensor"
    endpoint = "TestSensor"
    value = 42
    def get_value(self):
        rv = dict()
        rv['sensor_value'] = self.value
        return rv

    def get_unit(self):
        rv = dict()
        rv['unit'] = "Grad Celsius"
        return rv

    def set_value(self, value):
        self.value = value
        return self.get_value()