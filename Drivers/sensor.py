from . import Driver


class Sensor(Driver):
    __name__ = "Sensor"
    endpoint = "TemperaturSensor"

    def get_value(self):
        rv = dict()
        rv['sensor_value'] = 42
        return rv

    def get_unit(self):
        rv = dict()
        rv['unit'] = "Grad Celsius"
        return rv
