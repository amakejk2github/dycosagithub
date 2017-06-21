from . import Driver


class Sensortwo(Driver):
    __name__ = "Sensortwo"
    endpoint = "TemperaturSensor"

    def get_value(self):
        rv = dict()
        rv['sensor_value'] = 2
        return rv

    def get_unit(self):
        rv = dict()
        rv['unit'] = "Grad Celsius"
        return rv