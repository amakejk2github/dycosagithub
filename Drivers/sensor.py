from . import Driver
class Sensor(Driver):
    __name__ = "Sensor"

    def getValue(self):
        rv = dict()
        rv['sensor_value'] = 42
        return rv
    def getUnit(self):
        rv = dict()
        rv['unit'] = "Grad Celsius"
        return rv
