from . import Driver
class Sensor(Driver):
    __name__ = "Sensor"
    name = "Blafasel"

    def getValue(self):
        rv = dict()
        rv['sensor_value'] = 42
        return rv
    def getUnit(self):
        rv = dict()
        rv['unit'] = "Grad Celsius"
        return rv
