from . import Driver


class SensorLight(Driver):
    __name__ = "SensorLight"
    endpoint = "LichtSensor"

    def get_value(self):
        rv = dict()
        rv['sensor_value'] = 20000
        return rv

    def get_unit(self):
        rv = dict()
        rv['unit'] = "Lux"
        return rv