#pytest-test (execute with pytest in file directory)
import dycosa.drivers.sensor as sensor

s1 = sensor.Sensor()

def test_sensor():
    assert s1.get_value() == 42
    assert s1.get_unit() == "Grad Celsius"

