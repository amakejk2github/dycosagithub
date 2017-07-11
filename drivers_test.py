# pytest-test (execute with pytest in file directory)
from dycosa.drivers.sensor import Sensor

s1 = Sensor()


def test_sensor():
    assert s1.get_value()['sensor_value'] == 42
    assert s1.endpoint == "TemperaturSensor"
