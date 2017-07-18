import pytest
from dycosa.controller.controller import Controller


@pytest.fixture
def controller_prefab():
    con = Controller()
    return con


@pytest.mark.parametrize("test_attribute , expected_result", [
    ('Type', 'ESP-32'),
    ('Sleep', 1),
    ('Text', 'P6.302.1.2'),
    ('Name', 'Peter')
])
def test_get_config_function(controller_prefab, test_attribute, expected_result):
    assert controller_prefab.get_config(test_attribute) == expected_result


@pytest.mark.parametrize("test_attribute , test_entry, expected_result", [
    ('Type', 'Raspberry Pi', 'Raspberry Pi'),
    ('Sleep', 0, 0),
    #('Text', 'P7.2.03', 'P7.2.03'), failing due to settable false setting
    ('Name', 'Dieter', 'Dieter')
])
def test_set_config_function(controller_prefab, test_attribute, test_entry, expected_result):
    controller_prefab.set_config(test_attribute, test_entry)
    assert controller_prefab.get_config(test_attribute) == expected_result

def test_get_config_function_2(controller_prefab):
    with pytest.raises(Exception):
        controller_prefab.get_config("Permanent_power")

def test_set_config_function_2(controller_prefab):
    with pytest.raises(Exception):
        controller_prefab.set_config("Permanent_power" , 1)
